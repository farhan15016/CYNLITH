"""Minimal environment-backed application settings."""

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    """Runtime settings read from environment variables."""

    app_name: str
    app_version: str
    environment: str
    openai_api_key: str | None
    openai_model: str


@lru_cache
def get_settings() -> Settings:
    """Load settings once per process with safe local defaults."""
    return Settings(
        app_name=os.getenv("CYNLITH_APP_NAME", "Cynlith API"),
        app_version=os.getenv("CYNLITH_APP_VERSION", "0.1.0"),
        environment=os.getenv("CYNLITH_ENVIRONMENT", "local"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    )
