from langchain.agents import create_agent

from conf import GlobalLogger

from src.inf.env.env_conf import G_Settings

def create_translate_agent():
    translate_agent = create_agent(
        model=G_Settings.deepseek_api_chat_model,
    )

    return translate_agent
    


if __name__ == "__main__":
    try:
        GlobalLogger.info("hi")
    except Exception as e:
        GlobalLogger.error(e)
