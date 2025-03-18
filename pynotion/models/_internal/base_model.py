from __future__ import annotations as _annotations

from pydantic import BaseModel, ConfigDict


class BaseNotionModel(BaseModel):
    """Base class for Notion-like models with special read-only field handling."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_default=True,
        populate_by_name=True,
    )
