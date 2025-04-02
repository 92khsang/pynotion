from pydantic import BaseModel, ConfigDict


class BaseNotionModel(BaseModel):
    """Base class for Notion-like models with special read-only field handling."""

    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        validate_assignment=True,
    )


class FrozenNotionModel(BaseNotionModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        frozen=True,
    )
