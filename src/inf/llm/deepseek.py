from typing import List, Optional, Sequence, Dict
from openai import OpenAI

from conf import logger
from src.inf.env.env_conf import G_Settings


class DeepSeekLLMClient:
    """DeepSeek LLM 客户端, 提供对话响应接口"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化 DeepSeek LLM 客户端

        Args:
            api_key: DeepSeek API Key, 如果不提供则从环境变量读取
            base_url: API 基础 URL, 如果不提供则使用默认值
        """
        settings = G_Settings

        self.api_key = api_key or settings.deepseek_api_key
        self.base_url = base_url or settings.deepseek_api_url
        self.chat_model = settings.deepseek_api_chat_model

        if not self.api_key:
            raise ValueError("API Key 未配置, 请设置 DEEPSEEK_API_KEY 环境变量")

        # 初始化 OpenAI 客户端（兼容 DeepSeek API）
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        获取对话响应

        Args:
            messages: 对话消息列表，格式 [{"role": "user", "content": "..."}]
            model: 使用的模型, 如果不提供则使用默认模型
            stream: 是否使用流式响应
            temperature: 温度参数，控制随机性
            max_tokens: 最大输出token数

        Returns:
            str: 模型响应内容

        Raises:
            Exception: API 调用失败时抛出异常
        """
        if not messages:
            raise ValueError("消息列表不能为空")

        # 验证消息格式
        for message in messages:
            if not isinstance(message, dict) or "role" not in message or "content" not in message:
                raise ValueError("消息格式不正确，必须包含 'role' 和 'content' 字段")

        try:
            chat_model = model or self.chat_model

            # 准备请求参数
            request_params = {
                "model": chat_model,
                "messages": messages,
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
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        简单对话接口

        Args:
            prompt: 用户输入
            system_prompt: 系统提示词
            model: 使用的模型
            temperature: 温度参数
            max_tokens: 最大输出token数

        Returns:
            str: 模型响应内容
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        return self.chat_completion(
            messages=messages,
            model=model,
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
            "chat_model": self.chat_model
        }


# 创建默认客户端实例的工厂函数
def create_deepseek_client() -> DeepSeekLLMClient:
    """
    创建 DeepSeek 客户端实例

    Returns:
        DeepSeekLLMClient: DeepSeek 客户端实例
    """
    return DeepSeekLLMClient()


# 全局客户端实例（延迟初始化）
G_DeepSeekLLMClient = create_deepseek_client()


# 示例使用代码
if __name__ == "__main__":
    # 示例代码
    user_input = "你好，请介绍一下你自己"

    try:
        client = G_DeepSeekLLMClient

        # 打印客户端信息
        print("客户端信息:")
        info = client.get_client_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()

        # 简单对话
        print("用户输入:", user_input)
        response = client.simple_chat(
            prompt=user_input,
            system_prompt="你是一个 helpful assistant"
        )
        print("助手回复:", response)

        # 复杂对话示例
        print("\n" + "="*50)
        print("复杂对话示例:")
        messages = [
            {"role": "system", "content": "你是一个专业的Python编程助手"},
            {"role": "user", "content": "请解释一下Python的装饰器是什么"},
            {"role": "assistant", "content": "装饰器是Python中一种用于修改或扩展函数或类功能的工具..."},
            {"role": "user", "content": "能给一个具体的代码示例吗？"}
        ]

        response = client.chat_completion(messages=messages)
        print("助手回复:", response)

    except Exception as e:
        logger.error(f"错误: {e}")
