from __future__ import annotations

from typing import Annotated

from pydantic import Field, SecretStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    timeout_ms: Annotated[
        int, Field(ge=30_000, description="Request timeout in milliseconds")
    ] = 60_000

    base_url: Annotated[HttpUrl, Field(description="Base API URL")] = (
        "https://api.notion.com"
    )

    version: Annotated[str, Field(description="Notion API version")] = "2022-06-28"

    token: Annotated[
        SecretStr, Field(description="Notion API authentication token")
    ] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="NOTION_",
        extra="ignore",
        case_sensitive=False,
        validate_default=True,
    )


config = Config()
