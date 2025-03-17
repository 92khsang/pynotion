from __future__ import annotations as _annotations

from pydantic import BaseModel, ConfigDict, model_validator


class BaseNotionModel(BaseModel):
    """Base class for Notion-like models with special read-only field handling."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_default=True,
        populate_by_name=True,
    )

    __no_instance__ = False

    @model_validator(mode="before")
    @classmethod
    def validate_no_instance(cls, values):
        """Prevents instantiation of abstract classes."""
        if "__no_instance__" in cls.__dict__ and cls.__dict__["__no_instance__"]:
            raise TypeError(f"Cannot instantiate non-instance class {cls.__name__}")
        return values
