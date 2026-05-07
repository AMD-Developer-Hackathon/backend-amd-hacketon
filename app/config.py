from functools import lru_cache
from typing import Any

from pydantic import Field
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AMD Smart Product Assistant API"
    app_env: str = "local"
    debug: bool = True
    api_prefix: str = "/api"

    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/amd_smart_product_assistant",
        validation_alias="DATABASE_URL",
    )

    ai_provider: str = "mock"
    mock_model: str = "amd-smart-assistant-mock"
    vllm_base_url: str | None = None
    vllm_api_key: str | None = None
    vllm_model: str | None = None
    
    admin_api_key: str = Field(default="change-me", validation_alias="ADMIN_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: Any) -> Any:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "prod", "production"}:
                return False
            if normalized in {"local", "dev", "development"}:
                return True
        return value

    @field_validator("database_url", mode="after")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgresql://"):
            value = value.replace("postgresql://", "postgresql+psycopg://", 1)

        if "supabase.com" in value and "sslmode=" not in value:
            separator = "&" if "?" in value else "?"
            value = f"{value}{separator}sslmode=require"

        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
