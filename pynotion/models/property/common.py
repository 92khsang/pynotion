from typing import Literal, Optional, Annotated, TYPE_CHECKING, Union

from pydantic import (
    Field,
)

from pynotion.models.property.types import FormulaValueType
from .._internal import (
    FrozenNotionModel,
)

if TYPE_CHECKING:
    from pynotion.models.types import NotionDate

__all__ = [
    "StringFormulaValue",
    "NumberFormulaValue",
    "BooleanFormulaValue",
    "DateFormulaValue",
    "FormulaValue",
    "FORMULA_VALUE_CLASS_MAP",
]


class StringFormulaValue(FrozenNotionModel):
    """Represents a string formula value.

    Attributes:
        type: The type of the formula value.
        string: The string value.
    """

    type: Literal[FormulaValueType.STRING] = FormulaValueType.STRING
    string: Optional[str] = None


class NumberFormulaValue(FrozenNotionModel):
    """Represents a number formula value.

    Attributes:
        type: The type of the formula value.
        number: The number value.
    """

    type: Literal[FormulaValueType.NUMBER] = FormulaValueType.NUMBER
    number: Optional[float | int] = None


class BooleanFormulaValue(FrozenNotionModel):
    """Represents a boolean formula value.

    Attributes:
        type: The type of the formula value.
        boolean: The boolean value.
    """

    type: Literal[FormulaValueType.BOOLEAN] = FormulaValueType.BOOLEAN
    boolean: bool


class DateFormulaValue(FrozenNotionModel):
    """Represents a date formula value.

    Attributes:
        type: The type of the formula value.
        date: The date value.
    """

    type: Literal[FormulaValueType.DATE] = FormulaValueType.DATE
    date: Optional["NotionDate"] = None


FORMULA_VALUE_CLASS_MAP = {
    FormulaValueType.STRING: "StringFormulaValue",
    FormulaValueType.NUMBER: "NumberFormulaValue",
    FormulaValueType.BOOLEAN: "BooleanFormulaValue",
    FormulaValueType.DATE: "DateFormulaValue",
}

FormulaValue = Annotated[
    Union[tuple(FORMULA_VALUE_CLASS_MAP.values())], Field(discriminator="type")
]
