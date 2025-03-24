from __future__ import annotations as _annotations

from pydantic import BaseModel, ConfigDict


class BaseNotionModel(BaseModel):
    """Base class for Notion-like models with special read-only field handling."""

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        validate_assignment=True,
    )


class FrozenNotionModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        frozen=True,
    )
