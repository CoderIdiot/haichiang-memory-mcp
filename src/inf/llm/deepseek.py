import sys
from pathlib import Path
from ssl import get_default_verify_paths

from langsmith.run_trees import get_cached_client

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from typing import List, Optional, Sequence, Dict
from openai import OpenAI

from conf import logger
from src.inf.env.env_conf import G_Settings


class DeepSeekLLMClient:
    """DeepSeek LLM 客户端, 提供对话响应接口，支持thinking模型选择"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 use_thinking: Optional[bool] = None, thinking_model: Optional[str] = None,
                 no_thinking_model: Optional[str] = None):
        """
        初始化 DeepSeek LLM 客户端

        Args:
            api_key: DeepSeek API Key, 如果不提供则从环境变量读取
            base_url: API 基础 URL, 如果不提供则使用默认值
            use_thinking: 是否使用thinking模型，如果为None则根据配置默认值决定
            thinking_model: 指定thinking模型名称，如果为None则使用配置中的默认模型
            no_thinking_model: 指定非thinking模型名称，如果为None则使用配置中的默认模型
        """
        settings = G_Settings

        self.api_key = api_key or settings.deepseek_api_key
        self.base_url = base_url or settings.deepseek_api_url

        # 配置thinking模型相关参数
        self.thinking_model = thinking_model or settings.deepseek_thinking_model
        self.no_thinking_model = no_thinking_model or settings.deepseek_no_thinking_model

        # 确定默认使用thinking模型的策略
        if use_thinking is not None:
            self.default_use_thinking = use_thinking
        else:
            # 如果有配置的thinking模型，默认使用thinking模型
            self.default_use_thinking = bool(self.thinking_model)

        # 验证API Key
        if not self.api_key:
            raise ValueError("API Key 未配置, 请设置 DEEPSEEK_API_KEY 环境变量")

        # 验证至少有一个可用模型
        if not self.thinking_model and not self.no_thinking_model:
            logger.warning("未配置任何可用模型，请设置 DEEPSEEK_THINKING_MODEL 或 DEEPSEEK_NO_THINKING_MODEL")

        # 初始化 OpenAI 客户端（兼容 DeepSeek API）
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        logger.info(f"DeepSeek 客户端初始化完成，thinking模型: {self.thinking_model or '未配置'}, "
                   f"非thinking模型: {self.no_thinking_model or '未配置'}, "
                   f"默认使用thinking: {self.default_use_thinking}")

    def chat_completion(
        self,
        _messages: List[Dict[str, str]],
        model: Optional[str] = None,
        use_thinking: Optional[bool] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        获取对话响应

        Args:
            _messages: 对话消息列表，格式 [{"role": "user", "content": "..."}]
            model: 使用的模型, 如果不提供则根据use_thinking参数自动选择
            use_thinking: 是否使用thinking模型，如果为None则使用客户端默认设置
            stream: 是否使用流式响应
            temperature: 温度参数，控制随机性
            max_tokens: 最大输出token数

        Returns:
            str: 模型响应内容

        Raises:
            Exception: API 调用失败时抛出异常
        """
        if not _messages:
            raise ValueError("消息列表不能为空")

        # 验证消息格式
        for message in _messages:
            if not isinstance(message, dict) or "role" not in message or "content" not in message:
                raise ValueError("消息格式不正确，必须包含 'role' 和 'content' 字段")

        try:
            # 确定使用的模型
            if model:
                # 如果明确指定了模型，直接使用
                chat_model = model
            else:
                # 根据use_thinking参数选择模型
                if use_thinking is None:
                    use_thinking = self.default_use_thinking

                if use_thinking:
                    if not self.thinking_model:
                        logger.warning("未配置thinking模型，回退到非thinking模型")
                        chat_model = self.no_thinking_model
                    else:
                        chat_model = self.thinking_model
                else:
                    if not self.no_thinking_model:
                        logger.warning("未配置非thinking模型，回退到thinking模型")
                        chat_model = self.thinking_model
                    else:
                        chat_model = self.no_thinking_model

            # 验证模型是否可用
            if not chat_model:
                raise ValueError("无可用的模型配置，请检查 DEEPSEEK_THINKING_MODEL 或 DEEPSEEK_NO_THINKING_MODEL 配置")

            logger.debug(f"使用模型: {chat_model} (thinking: {use_thinking})")

            # 准备请求参数
            request_params = {
                "model": chat_model,
                "messages": _messages,
                "stream": stream
            }

            # 添加可选参数
            if temperature is not None:
                request_params["temperature"] = temperature
            if max_tokens is not None:
                request_params["max_tokens"] = max_tokens

            # 调用对话 API
            completion = self.client.chat.completions.create(**request_params)

            # 处理响应
            if stream:
                # 流式响应 - 返回生成器
                def stream_generator():
                    for chunk in completion:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content

                return "".join(stream_generator())
            else:
                # 非流式响应
                return completion.choices[0].message.content

        except Exception as e:
            raise Exception(f"对话响应失败: {str(e)}")

    def simple_chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        use_thinking: Optional[bool] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        简单对话接口

        Args:
            prompt: 用户输入
            system_prompt: 系统提示词
            model: 使用的模型，如果为None则根据use_thinking参数自动选择
            use_thinking: 是否使用thinking模型，如果为None则使用客户端默认设置
            temperature: 温度参数
            max_tokens: 最大输出token数

        Returns:
            str: 模型响应内容
        """
        _messages = []

        if system_prompt:
            _messages.append({"role": "system", "content": system_prompt})

        _messages.append({"role": "user", "content": prompt})

        return self.chat_completion(
            _messages=_messages,
            model=model,
            use_thinking=use_thinking,
            stream=False,
            temperature=temperature,
            max_tokens=max_tokens
        )

    def get_client_info(self) -> Dict[str, str]:
        """
        获取客户端信息

        Returns:
            Dict[str, str]: 客户端配置信息
        """
        return {
            "api_key": "***" + self.api_key[-4:] if self.api_key else "未配置",
            "base_url": self.base_url,
            "thinking_model": self.thinking_model or "未配置",
            "no_thinking_model": self.no_thinking_model or "未配置",
            "default_use_thinking": str(self.default_use_thinking)
        }


# 创建默认客户端实例的工厂函数
def create_deepseek_client(**kwargs) -> DeepSeekLLMClient:
    """
    创建 DeepSeek 客户端实例

    Args:
        **kwargs: 传递给 DeepSeekLLMClient.__init__ 的参数

    Returns:
        DeepSeekLLMClient: DeepSeek 客户端实例
    """
    return DeepSeekLLMClient(**kwargs)


# 全局客户端实例（延迟初始化）
G_DeepSeekLLMClient = create_deepseek_client()


# 示例使用代码
if __name__ == "__main__":
    # 示例代码
    user_input = "你好，请介绍一下你自己"
    complex_question = "请分析一下时间复杂度为O(n log n)的排序算法的原理和适用场景"

    try:
        client = G_DeepSeekLLMClient

        # 打印客户端信息
        print("客户端信息:")
        info = client.get_client_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()

        # 简单对话（使用默认模型）
        print("=== 简单对话示例 ===")
        print("用户输入:", user_input)
        response = client.simple_chat(
            prompt=user_input,
            system_prompt="你是一个 helpful assistant"
        )
        print("助手回复:", response)

        # 使用thinking模型回答复杂问题
        print("\n=== Thinking模型示例 ===")
        print("复杂问题:", complex_question)
        response_thinking = client.simple_chat(
            prompt=complex_question,
            system_prompt="你是一个专业的算法分析师，请详细分析问题",
            use_thinking=True
        )
        print("Thinking模型回复:", response_thinking)

        # 使用非thinking模型回答相同问题
        print("\n=== 非Thinking模型对比 ===")
        response_no_thinking = client.simple_chat(
            prompt=complex_question,
            system_prompt="你是一个专业的算法分析师，请详细分析问题",
            use_thinking=False
        )
        print("非Thinking模型回复:", response_no_thinking)

        # 复杂对话示例
        print("\n" + "="*50)
        print("多轮对话示例:")
        messages = [
            {"role": "system", "content": "你是一个专业的Python编程助手"},
            {"role": "user", "content": "请解释一下Python的装饰器是什么"},
            {"role": "assistant", "content": "装饰器是Python中一种用于修改或扩展函数或类功能的工具..."},
            {"role": "user", "content": "能给一个具体的代码示例吗？"}
        ]

        response = client.chat_completion(_messages=messages, use_thinking=True)
        print("助手回复:", response)

    except Exception as e:
        logger.error(f"错误: {e}")
