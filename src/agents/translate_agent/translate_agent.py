from conf import logger

from src.inf.llm.deepseek import G_DeepSeekLLMClient

if __name__ == '__main__':
    try:
        logger.info('hi')
    except Exception as e:
        logger.error(e)
