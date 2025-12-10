"""
Qwen LLM 客户端模块
提供基于阿里云百炼的向量生成服务
"""

from typing import List, Optional, Sequence, Dict
from openai import OpenAI

from conf import GlobalLogger
from src.inf.env.env_conf import G_Settings



class QwenLLMClient:
    """Qwen LLM 客户端, 提供向量生成接口"""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化 Qwen LLM 客户端

        Args:
            api_key: 阿里云百炼 API Key, 如果不提供则从环境变量读取
            base_url: API 基础 URL, 如果不提供则使用默认值
        """
        settings = G_Settings

        self.api_key = api_key or settings.qwen_api_key
        self.base_url = base_url or settings.qwen_api_url
        self.embedding_model = settings.qwen_api_embedding_model

        if not self.api_key:
            raise ValueError("API Key 未配置, 请设置 DASHSCOPE_API_KEY 环境变量")

        # 初始化 OpenAI 客户端（兼容阿里云百炼 API）
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    
    def get_embedding_vector(self, texts: Sequence[str], model: Optional[str] = None) -> List[List[float]]:
        """
        获取文本序列的向量数据（批量处理接口）

        Args:
            texts: 输入文本序列
            model: 使用的向量模型

        Returns:
            List[List[float]]: 向量数据列表
        """
        if not texts:
            return []

        # 如果是单个文本，转换为列表格式
        if isinstance(texts, str):
            texts = [texts]

        # 过滤空文本
        valid_texts = [text.strip() for text in texts if text.strip()]
        if not valid_texts:
            return []

        try:
            embedding_model = model or self.embedding_model

            # 直接调用客户端的 embeddings API
            completion = self.client.embeddings.create(
                model=embedding_model,
                input=valid_texts
            )

            # 提取向量数据
            return [item.embedding for item in completion.data]

        except Exception as e:
            raise Exception(f"向量生成失败: {str(e)}")

    def get_client_info(self) -> Dict[str, str]:
        """
        获取客户端信息

        Returns:
            Dict[str, str]: 客户端配置信息
        """
        return {
            "api_key": "***" + self.api_key[-4:] if self.api_key else "未配置",
            "base_url": self.base_url,
            "embedding_model": self.embedding_model
        }


# 创建默认客户端实例的工厂函数
def create_qwen_client() -> QwenLLMClient:
    """
    创建 Qwen 客户端实例

    Returns:
        QwenLLMClient: Qwen 客户端实例
    """
    return QwenLLMClient()


# 全局客户端实例（延迟初始化）
G_QwenLLMClient = create_qwen_client()


# 示例使用代码
if __name__ == "__main__":
    # 示例代码
    input_text = "衣服的质量杠杠的"

    try:
        client = G_QwenLLMClient

        # 打印客户端信息
        print("客户端信息:")
        info = client.get_client_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        print()

        # 获取向量数据
        vectors = client.get_embedding_vector([input_text])
        vector = vectors[0]  # 获取第一个文本的向量
        print(f"\n向量维度: {len(vector)}")
        print(f"前5个值: {vector[:5]}")

    except Exception as e:
        GlobalLogger.error(f"错误: {e}")