"""
Qwen 向量生成演示
展示如何使用 QwenLLMClient 进行文本向量生成
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from inf.llm.qwen import create_qwen_client


def main():
    """主函数，演示 Qwen 向量生成功能"""

    # 测试文本
    test_texts = [
        "衣服的质量杠杠的",
        "这件商品物美价廉",
        "物流速度很快，包装也很好",
        "客服态度友善，解决问题及时"
    ]

    try:
        # 创建 Qwen 客户端
        print("正在初始化 Qwen 客户端...")
        client = create_qwen_client()

        # 显示客户端配置信息
        print("\n=== 客户端配置信息 ===")
        info = client.get_client_info()
        for key, value in info.items():
            print(f"{key}: {value}")

        print(f"\n=== 向量生成演示 ===")

        # 单个文本向量生成
        print("\n1. 单个文本向量生成:")
        text = test_texts[0]
        print(f"输入文本: {text}")

        response = client.generate_embedding(text)
        print(f"使用模型: {response.model}")
        print(f"向量维度: {len(response.data[0]['embedding'])}")
        print(f"Token 使用情况: {response.usage}")

        # 批量向量生成
        print("\n2. 批量文本向量生成:")
        print(f"输入文本数量: {len(test_texts)}")

        batch_response = client.generate_batch_embeddings(test_texts)
        print(f"使用模型: {batch_response.model}")
        print(f"生成向量数量: {len(batch_response.data)}")
        print(f"总 Token 使用情况: {batch_response.usage}")

        # 显示每个文本的向量维度
        print("\n各文本向量维度:")
        for i, (text, data) in enumerate(zip(test_texts, batch_response.data)):
            vector_length = len(data['embedding'])
            print(f"  文本 {i+1} ({text[:20]}...): {vector_length} 维")

        # 简化接口演示
        print("\n3. 简化接口演示:")
        text = "欢迎使用 Qwen 向量服务"
        vector = client.get_embedding_vector(text)
        print(f"文本: {text}")
        print(f"向量长度: {len(vector)}")
        print(f"向量前5个值: {vector[:5]}")
        print(f"向量后5个值: {vector[-5:]}")

        print("\n=== 演示完成 ===")

    except Exception as e:
        print(f"演示过程中发生错误: {e}")
        print("\n请检查以下配置:")
        print("1. 环境变量 DASHSCOPE_API_KEY 是否正确设置")
        print("2. 网络连接是否正常")
        print("3. API Key 是否有效且额度充足")


if __name__ == "__main__":
    main()