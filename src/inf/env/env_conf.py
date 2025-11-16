import sys
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv, main

# Get project root directory (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Add project root to Python path if not already present
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Load .env file using absolute path
load_dotenv(PROJECT_ROOT / ".env")

# Import logger from conf
try:
    from conf import logger
except ImportError:
    # Fallback: if conf import fails, use basic logging
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Global settings class"""

    # Application settings
    app_name: str = Field(default="hc-mem", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")

    # DeepSeek configuration
    deepseek_api_url: str = Field(default='', alias="DEEPSEEK_API_URL")
    deepseek_api_key: str = Field(default='', alias="DEEPSEEK_API_KEY")
    deepseek_thinking_model: str = Field(default="", alias="DEEPSEEK_THINKING_MODEL")
    deepseek_no_thinking_model: str = Field(default="", alias="DEEPSEEK_NO_THINKING_MODEL")

    # Qwen configuration
    qwen_api_url: str = Field(default="", alias="DASHSCOPE_BASE_URL")
    qwen_api_key: str = Field(default='', alias="DASHSCOPE_API_KEY")
    qwen_api_embedding_model: str = Field(default="text-embedding-v4", alias="QWEN_EMBEDDING_MODEL")
    qwen_api_embedding_dim: int = Field(default=1024, alias="QWEN_EMBEDDING_DIM")


    model_config = {
        "env_file": str(PROJECT_ROOT / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "populate_by_name": True
    }


# Create global settings instance
G_Settings = Settings()


if __name__ == "__main__":
    try:
        logger.info("Loading .env file...")
        logger.info(f'Global Settings: {G_Settings}')
        logger.info("Settings loaded successfully")
    except Exception as e:
        logger.error(f"Error loading .env file: {e}")
