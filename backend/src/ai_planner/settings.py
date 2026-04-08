from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = Field(default="AI Smart Planner", alias="NAME")
    debug: bool = Field(default=False, alias="DEBUG")
    address: str = Field(default="0.0.0.0", alias="ADDRESS")
    port: int = Field(default=8000, alias="PORT")
    reload: bool = Field(default=False, alias="RELOAD")
    cors_origins: list[str] = Field(default=["*"], alias="CORS_ORIGINS")

    # Qwen API (OAuth authentication)
    qwen_api_base: str = Field(default="https://portal.qwen.ai/v1", alias="QWEN_API_BASE")
    qwen_model: str = Field(default="qwen3-coder-plus", alias="QWEN_MODEL")
    
    # OAuth credentials path
    qwen_creds_file: Path = Field(default=Path.home() / ".qwen" / "oauth_creds.json", alias="QWEN_CREDS_FILE")

    # Database (V2)
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="ai_planner", alias="DB_NAME")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(default="postgres", alias="DB_PASSWORD")


settings = Settings.model_validate({})
