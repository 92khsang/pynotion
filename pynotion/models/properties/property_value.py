from __future__ import annotations as _annotations

from typing import Literal, Optional, Annotated

from pydantic import (
    Field,
    field_validator,
    BeforeValidator,
    field_serializer,
)

from .types import (
    PropertyType,
    FormulaValueType,
    RollupValueType,
)
from .._internal import (
    BaseNotionModel,
    validate_phone,
    validate_email,
    validate_url,
    FrozenNotionModel,
)
from ..file import FileWithName
from ..object import NotionObjectId
from ..rich_text import RxRichText, TxRichText
from ..types import Color, NotionDate, NotionDatetime
from ..user import User, UserRef


class StringFormulaValue(FrozenNotionModel):
    type: Literal[FormulaValueType.STRING] = Field(
        default=FormulaValueType.STRING, frozen=True
    )
    string: Optional[str] = None


class NumberFormulaValue(FrozenNotionModel):
    type: Literal[FormulaValueType.NUMBER] = Field(
        default=FormulaValueType.NUMBER, frozen=True
    )
    number: Optional[float | int] = None


class BooleanFormulaValue(FrozenNotionModel):
    type: Literal[FormulaValueType.BOOLEAN] = Field(
        default=FormulaValueType.BOOLEAN, frozen=True
    )
    boolean: bool


class DateFormulaValue(FrozenNotionModel):
    type: Literal[FormulaValueType.DATE] = Field(
        default=FormulaValueType.DATE, frozen=True
    )
    date: Optional[NotionDate] = None


FormulaValue = Annotated[
    StringFormulaValue | NumberFormulaValue | BooleanFormulaValue | DateFormulaValue,
    Field(discriminator="type"),
]


class ArrayRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.ARRAY] = RollupValueType.ARRAY
    array: Optional[list[RxPropertyValue]] = None


class DateRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.DATE] = RollupValueType.DATE
    date: Optional[NotionDate] = None


class IncompleteRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.INCOMPLETE] = RollupValueType.INCOMPLETE
    incomplete: Optional[dict] = None


class NumberRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.NUMBER] = RollupValueType.NUMBER
    number: Optional[float | int] = None


class UnsupportedRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.UNSUPPORTED] = RollupValueType.UNSUPPORTED
    unsupported: Optional[dict] = None


RollupValue = Annotated[
    ArrayRollupValue
    | DateRollupValue
    | IncompleteRollupValue
    | NumberRollupValue
    | UnsupportedRollupValue,
    Field(discriminator="type"),
]


class UniqueIdValue(BaseNotionModel):
    number: int
    prefix: Optional[str] = None


class UnverifiedValue(BaseNotionModel):
    state: Literal["unverified"] = "unverified"
    verified_by: None = None
    date: None = None


class VerifiedValue(BaseNotionModel):
    state: Literal["verified"] = "verified"
    verified_by: User
    date: NotionDate


VerificationValue = Annotated[
    VerifiedValue | UnverifiedValue,
    Field(discriminator="state"),
]


class RxOptionValue(FrozenNotionModel):
    id: str
    name: str
    color: Color


class _RxBasePropertyValue(FrozenNotionModel):
    id: str


class CreatedByPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.CREATED_BY] = PropertyType.CREATED_BY
    created_by: User


class CreatedTimePropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.CREATED_TIME] = PropertyType.CREATED_TIME
    created_time: NotionDatetime


class LastEditedByPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.LAST_EDITED_BY] = PropertyType.LAST_EDITED_BY
    last_edited_by: User


class LastEditedTimePropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.LAST_EDITED_TIME] = PropertyType.LAST_EDITED_TIME
    last_edited_time: NotionDatetime


class RollupPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.ROLLUP] = PropertyType.ROLLUP
    rollup: RollupValue


class FormulaPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.FORMULA] = PropertyType.FORMULA
    formula: FormulaValue


class UniqueIdPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.UNIQUE_ID] = PropertyType.UNIQUE_ID
    unique_id: UniqueIdValue


class VerificationPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.VERIFICATION] = PropertyType.VERIFICATION
    verification: VerificationValue


class RxCheckboxPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.CHECKBOX] = PropertyType.CHECKBOX
    checkbox: bool


class RxDatePropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.DATE] = PropertyType.DATE
    date: Optional[NotionDate] = None


class RxEmailPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.EMAIL] = PropertyType.EMAIL
    email: Optional[Annotated[str, BeforeValidator(validate_email)]] = None


class RxFilesPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.FILES] = PropertyType.FILES
    files: list[FileWithName]


class RxMultiSelectPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.MULTI_SELECT] = PropertyType.MULTI_SELECT
    multi_select: list[RxOptionValue]


class RxNumberPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.NUMBER] = PropertyType.NUMBER
    number: Optional[float | int] = None


class RxPeoplePropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.PEOPLE] = PropertyType.PEOPLE
    people: list[User]


class RxPhoneNumberPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.PHONE_NUMBER] = PropertyType.PHONE_NUMBER
    phone_number: Optional[Annotated[str, BeforeValidator(validate_phone)]] = None


class RxRelationPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.RELATION] = PropertyType.RELATION
    relation: list[NotionObjectId]
    has_more: bool


class RxRichTextPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.RICH_TEXT] = PropertyType.RICH_TEXT
    rich_text: list[RxRichText]


class RxSelectPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.SELECT] = PropertyType.SELECT
    select: Optional[RxOptionValue] = None


class RxStatusPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.STATUS] = PropertyType.STATUS
    status: Optional[RxOptionValue] = None


class RxTitlePropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.TITLE] = PropertyType.TITLE
    title: list[RxRichText]


class RxUrlPropertyValue(_RxBasePropertyValue):
    type: Literal[PropertyType.URL] = PropertyType.URL
    url: Optional[Annotated[str, BeforeValidator(validate_url)]] = None


RxPropertyValue = Annotated[
    CreatedByPropertyValue
    | CreatedTimePropertyValue
    | LastEditedByPropertyValue
    | LastEditedTimePropertyValue
    | FormulaPropertyValue
    | UniqueIdPropertyValue
    | VerificationPropertyValue
    | RxCheckboxPropertyValue
    | RxDatePropertyValue
    | RxEmailPropertyValue
    | RxFilesPropertyValue
    | RxMultiSelectPropertyValue
    | RxNumberPropertyValue
    | RxPeoplePropertyValue
    | RxPhoneNumberPropertyValue
    | RxRelationPropertyValue
    | RollupPropertyValue
    | RxRichTextPropertyValue
    | RxSelectPropertyValue
    | RxStatusPropertyValue
    | RxTitlePropertyValue
    | RxUrlPropertyValue,
    Field(discriminator="type"),
]


class TxOptionValue(BaseNotionModel):
    name: str

    @field_validator("name", mode="after")
    def validate_name_field(cls, v):
        if "," in v:
            raise ValueError("Comma is not allowed in the name field")
        return v


class TxCheckboxPropertyValue(BaseNotionModel):
    checkbox: bool


class TxDatePropertyValue(BaseNotionModel):
    date: NotionDate


class TxEmailPropertyValue(BaseNotionModel):
    email: Annotated[str, BeforeValidator(validate_email)]


class TxFilesPropertyValue(BaseNotionModel):
    files: list[FileWithName] = Field(default_factory=list)


class TxMultiSelectPropertyValue(BaseNotionModel):
    multi_select: list[TxOptionValue] = Field(default_factory=list)


class TxNumberPropertyValue(BaseNotionModel):
    number: Optional[float | int]


class TxPeoplePropertyValue(BaseNotionModel):
    people: list[UserRef] = Field(default_factory=list)


class TxPhoneNumberPropertyValue(BaseNotionModel):
    phone_number: Annotated[str, BeforeValidator(validate_phone)]


class TxRelationPropertyValue(BaseNotionModel):
    relation: list[NotionObjectId] = Field(default_factory=list)


class TxRichTextPropertyValue(BaseNotionModel):
    rich_text: list[TxRichText] = Field(default_factory=list)

    @field_serializer("rich_text")
    def ser_rich_text(self, value, _):
        return [text.model_dump(exclude={"type"}) for text in value]


class TxSelectPropertyValue(BaseNotionModel):
    select: TxOptionValue


class TxStatusPropertyValue(BaseNotionModel):
    status: TxOptionValue


class TxTitlePropertyValue(BaseNotionModel):
    title: list[TxRichText] = Field(default_factory=list)

    @field_serializer("title")
    def ser_title(self, value, _):
        return [text.model_dump(exclude={"type"}) for text in value]


class TxUrlPropertyValue(BaseNotionModel):
    url: Annotated[str, BeforeValidator(validate_url)]


TxPropertyValue = (
    TxCheckboxPropertyValue
    | TxDatePropertyValue
    | TxEmailPropertyValue
    | TxFilesPropertyValue
    | TxMultiSelectPropertyValue
    | TxNumberPropertyValue
    | TxPeoplePropertyValue
    | TxPhoneNumberPropertyValue
    | TxRelationPropertyValue
    | TxRichTextPropertyValue
    | TxSelectPropertyValue
    | TxStatusPropertyValue
    | TxTitlePropertyValue
    | TxUrlPropertyValue
)
