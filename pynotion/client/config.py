from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class NotionClientConfig(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
    )

    base_url: str = Field(default="https://api.notion.com/v1")
    version: str = Field(default="2022-06-28")
    timeout_ms: Annotated[int, Field(ge=30_000)] = 60_000
    token: str
