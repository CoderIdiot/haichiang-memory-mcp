from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Get project root directory (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Load .env file using absolute path
load_dotenv(PROJECT_ROOT / ".env")


class Settings(BaseSettings):
    """Global settings class"""

    # Application settings
    app_name: str = Field(default="hc-mem", validation_alias="APP_NAME")
    app_version: str = Field(default="0.1.0", validation_alias="APP_VERSION")
    debug: bool = Field(default=False, validation_alias="DEBUG")

    # DeepSeek configuration
    deepseek_api_url: str = Field(
        default="https://api.deepseek.cn/v1/chat/completions",
        validation_alias="DEEPSEEK_API_URL"
    )
    deepseek_api_key: Optional[str] = Field(default=None, validation_alias="DEEPSEEK_API_KEY")
    deepseek_api_model: str = Field(default="deepseek-3.5", validation_alias="DEEPSEEK_API_MODEL")

    # Qwen configuration
    qwen_api_url: str = Field(
        default="https://api.deepseek.cn/v1/chat/completions",
        validation_alias="Qwen_API_URL"
    )
    qwen_api_key: Optional[str] = Field(default=None, validation_alias="Qwen_API_KEY")
    qwen_api_embedding_model: str = Field(default="qwen-3.5", validation_alias="Qwen_API_EMBEDDING_MODEL")


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