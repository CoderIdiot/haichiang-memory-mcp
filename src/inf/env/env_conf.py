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
    app_name: str = Field(default="hc-mem", validation_alias="APP_NAME")
    app_version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
    debug: bool = Field(default=False, validation_alias="DEBUG")

    # DeepSeek configuration
    deepseek_api_url: str = Field(default='', validation_alias="DEEPSEEK_API_URL")
    deepseek_api_key: str = Field(default='', validation_alias="DEEPSEEK_API_KEY")
    deepseek_api_model: str = Field(default="", validation_alias="DEEPSEEK_API_MODEL")

    # Qwen configuration
    qwen_api_url: str = Field(default='', validation_alias="Qwen_API_URL")
    qwen_api_key: str = Field(default='', validation_alias="Qwen_API_KEY")
    qwen_api_embedding_model: str = Field(default="", validation_alias="Qwen_API_EMBEDDING_MODEL")


    model_config = {
        "env_file": str(PROJECT_ROOT / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


# Create global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance"""
    return settings

if __name__ == "__main__":
    try:
        settings = Settings()
        logger.info("Settings loaded successfully")
    except Exception as e:
        logger.error(f"Error loading .env file: {e}")
