from __future__ import annotations as _annotations

from collections import OrderedDict

from pydantic import BaseModel, ConfigDict, model_serializer


class BaseNotionModel(BaseModel):
    """Base class for Notion-like models with special read-only field handling."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_default=True,
        populate_by_name=True,
    )

    # Class variable for serializable private attributes
    __serializable_private_attrs__: dict = {}

    def __new__(cls, *args, **kwargs):
        if cls is BaseNotionModel:
            raise TypeError(f"{cls.__name__} cannot be instantiated directly")
        return super().__new__(cls)

    @classmethod
    def _collect_all_annotation(cls) -> dict:
        """Returns a list of all annotations for the class."""
        all_annotations = {}
        for clz in reversed(cls.__mro__):
            if hasattr(clz, '__annotations__'):
                all_annotations.update(clz.__annotations__)

        return all_annotations

    @model_serializer(mode="wrap")
    def serialize_model(self, nxt) -> OrderedDict:
        """Ensures private attributes are included and field order is preserved."""
        data = nxt(self)

        # Get private attributes that should be serialized
        private_attrs = {
            attr: getattr(self, attr)
            for attr in self.__serializable_private_attrs__
            if attr in self.__private_attributes__
        }

        # Maintain field declaration order
        all_annotations = self._collect_all_annotation()

        # Use the collected fields for ordering
        declared_fields = list(all_annotations.keys())
        ordered_data = OrderedDict()

        # Process fields in their declaration order
        for field in declared_fields:
            if field in private_attrs:
                alias = self.__serializable_private_attrs__[field]
                ordered_data[alias] = private_attrs.pop(field)
            elif field in data:
                ordered_data[field] = data[field]

        # Add any remaining private attributes
        ordered_data.update(
            {
                self.__serializable_private_attrs__[k]: v
                for k, v in private_attrs.items()
                if k not in ordered_data
            }
        )

        return ordered_data
