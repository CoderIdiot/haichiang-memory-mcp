from conf import GlobalLogger

from src.inf.llm.deepseek import G_DeepSeekLLMClient

if __name__ == "__main__":
    try:
        GlobalLogger.info("hi")
    except Exception as e:
        GlobalLogger.error(e)
