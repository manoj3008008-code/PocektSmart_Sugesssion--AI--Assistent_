from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    environment: str = "development"
    secret_key: str = "change-this-secret-key"
    database_url: str = "sqlite:///./pocketsmart.db"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    use_mock_ai: bool = True

    allowed_origins: List[str] = ["http://127.0.0.1:8000", "http://localhost:8000"]
    max_image_mb: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str):
            return [x.strip() for x in value.split(",") if x.strip()]
        return value

settings = Settings()

if settings.gemini_api_key:
    settings.use_mock_ai = False
