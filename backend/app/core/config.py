"""Application settings loaded from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly typed runtime settings for backend components."""

    app_name: str = "Invoice Escalation System"
    env: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./invoice_escalation.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
