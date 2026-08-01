"""Application settings loaded from environment / backend/.env."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/app/core/config.py -> repo root is parents[3]
REPO_ROOT = Path(__file__).resolve().parents[3]
BACKEND_DIR = REPO_ROOT / "backend"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="FarmCredit AI", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        alias="CORS_ORIGINS",
    )

    model_dir: str = Field(default="ml/artifacts/model", alias="MODEL_DIR")
    demo_farmers_path: str = Field(
        default="backend/app/data/demo_farmers.json",
        alias="DEMO_FARMERS_PATH",
    )
    demo_cache_dir: str = Field(
        default="backend/app/data/demo_cache",
        alias="DEMO_CACHE_DIR",
    )

    hf_model_id: str = Field(
        default="your-hf-username/farmcredit-ai-mistral-7b",
        alias="HF_MODEL_ID",
    )
    hf_token: str | None = Field(default=None, alias="HF_TOKEN")
    hf_base_model: str = Field(
        default="mistralai/Mistral-7B-Instruct-v0.3",
        alias="HF_BASE_MODEL",
    )

    llm_enabled: bool = Field(default=False, alias="LLM_ENABLED")
    llm_load_in_4bit: bool = Field(default=True, alias="LLM_LOAD_IN_4BIT")
    llm_eager_load: bool = Field(default=False, alias="LLM_EAGER_LOAD")
    llm_max_new_tokens: int = Field(default=320, alias="LLM_MAX_NEW_TOKENS")
    llm_temperature: float = Field(default=0.4, alias="LLM_TEMPERATURE")

    demo_use_cache_by_default: bool = Field(
        default=True,
        alias="DEMO_USE_CACHE_BY_DEFAULT",
    )

    @field_validator("hf_token", mode="before")
    @classmethod
    def empty_token_as_none(cls, value: object) -> object:
        if value is None:
            return None
        if isinstance(value, str) and value.strip() == "":
            return None
        return value

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def resolve_path(self, relative_or_absolute: str) -> Path:
        path = Path(relative_or_absolute)
        if path.is_absolute():
            return path
        return (REPO_ROOT / path).resolve()

    @property
    def model_dir_path(self) -> Path:
        return self.resolve_path(self.model_dir)

    @property
    def demo_farmers_file(self) -> Path:
        return self.resolve_path(self.demo_farmers_path)

    @property
    def demo_cache_path(self) -> Path:
        return self.resolve_path(self.demo_cache_dir)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
