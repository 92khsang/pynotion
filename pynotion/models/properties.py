from __future__ import annotations as _annotations

from datetime import datetime
from enum import Enum
from typing import Literal, Optional, Annotated
from uuid import UUID

from pydantic import (
    Field,
    field_validator,
    BeforeValidator,
    Discriminator,
    Tag,
)

from ._internal import (
    BaseNotionModel,
    validate_uuid4,
    validate_datetime,
    validate_phone,
    validate_email,
    validate_url,
)
from .file import FileWithName
from .object import NotionObjectId
from .rich_text import RichText
from .types import NotionEquation, Color, NotionDate
from .user import User


class PropertyType(str, Enum):
    CHECKBOX = "checkbox"
    CREATED_BY = "created_by"
    CREATED_TIME = "created_time"
    DATE = "date"
    EMAIL = "email"
    FILES = "files"
    FORMULA = "formula"
    LAST_EDITED_BY = "last_edited_by"
    LAST_EDITED_TIME = "last_edited_time"
    MULTI_SELECT = "multi_select"
    NUMBER = "number"
    PEOPLE = "people"
    PHONE_NUMBER = "phone_number"
    RELATION = "relation"
    RICH_TEXT = "rich_text"
    ROLLUP = "rollup"
    SELECT = "select"
    STATUS = "status"
    TITLE = "title"
    URL = "url"
    UNIQUE_ID = "unique_id"
    VERIFICATION = "verification"


class NumberFormat(str, Enum):
    ARGENTINE_PESO = "argentine_peso"
    BAHT = "baht"
    AUSTRALIAN_DOLLAR = "australian_dollar"
    CANADIAN_DOLLAR = "canadian_dollar"
    CHILEAN_PESO = "chilean_peso"
    COLOMBIAN_PESO = "colombian_peso"
    DANISH_KRONE = "danish_krone"
    DIRHAM = "dirham"
    DOLLAR = "dollar"
    EURO = "euro"
    FORINT = "forint"
    FRANC = "franc"
    HONG_KONG_DOLLAR = "hong_kong_dollar"
    KORUNA = "koruna"
    KRONA = "krona"
    LEU = "leu"
    LIRA = "lira"
    MEXICAN_PESO = "mexican_peso"
    NEW_TAIWAN_DOLLAR = "new_taiwan_dollar"
    NEW_ZEALAND_DOLLAR = "new_zealand_dollar"
    NORWEGIAN_KRONE = "norwegian_krone"
    NUMBER = "number"
    NUMBER_WITH_COMMAS = "number_with_commas"
    PERCENT = "percent"
    PHILIPPINE_PESO = "philippine_peso"
    POUND = "pound"
    PERUVIAN_SOL = "peruvian_sol"
    RAND = "rand"
    REAL = "real"
    RINGGIT = "ringgit"
    RIYAL = "riyal"
    RUBLE = "ruble"
    RUPEE = "rupee"
    RUPIAH = "rupiah"
    SHEKEL = "shekel"
    SINGAPORE_DOLLAR = "singapore_dollar"
    URUGUAYAN_PESO = "uruguayan_peso"
    YEN = "yen"
    YUAN = "yuan"
    WON = "won"
    ZLOTY = "zloty"


class RollupFunction(str, Enum):
    AVERAGE = "average"
    CHECKED = "checked"
    COUNT = "count"
    COUNT_PER_GROUP = "count_per_group"
    COUNT_VALUES = "count_values"
    DATE_RANGE = "date_range"
    EARLIEST_DATE = "earliest_date"
    EMPTY = "empty"
    LATEST_DATE = "latest_date"
    MAX = "max"
    MEDIAN = "median"
    MIN = "min"
    NOT_EMPTY = "not_empty"
    PERCENT_CHECKED = "percent_checked"
    PERCENT_EMPTY = "percent_empty"
    PERCENT_NOT_EMPTY = "percent_not_empty"
    PERCENT_PER_GROUP = "percent_per_group"
    PERCENT_UNCHECKED = "percent_unchecked"
    RANGE = "range"
    SHOW_ORIGINAL = "show_original"
    SHOW_UNIQUE = "show_unique"
    SUM = "sum"
    UNCHECKED = "unchecked"
    UNIQUE = "unique"


class FormulaValueType(str, Enum):
    BOOLEAN = "boolean"
    DATE = "date"
    NUMBER = "number"
    STRING = "string"


class RollupValueType(str, Enum):
    ARRAY = "array"
    DATE = "date"
    INCOMPLETE = "incomplete"
    NUMBER = "number"
    UNSUPPORTED = "unsupported"


class BaseOption(BaseNotionModel):
    id: str
    name: str
    color: Optional[Color] = Field(default=None)

    @field_validator("name", mode="after")
    def validate_name_field(cls, v):
        if "," in v:
            raise ValueError("Comma is not allowed in the name field")
        return v


class SelectOptions(BaseNotionModel):
    options: Optional[list[BaseOption]] = Field(default=None)


class Number(BaseNotionModel):
    format: Optional[NumberFormat] = Field(default=None)


class DualProperty(BaseNotionModel):
    synced_property_id: str
    synced_property_name: str


class Relation(BaseNotionModel):
    database_id: NotionObjectId
    dual_property: Optional[DualProperty] = Field(default=None)


class Rollup(BaseNotionModel):
    relation_property_name: str
    relation_property_id: str
    rollup_property_name: str
    rollup_property_id: str
    function: RollupFunction


class StatusOptions(BaseNotionModel):
    options: Optional[list[BaseOption]] = Field(default=None)


class GroupOption(BaseOption):
    option_ids: Optional[
        list[Annotated[str | int | bytes | UUID, BeforeValidator(validate_uuid4)]]
    ] = Field(default=None)


class _BaseProperty(BaseNotionModel):
    id: str
    name: str


class CheckboxProperty(_BaseProperty):
    type: Literal[PropertyType.CHECKBOX] = Field(
        default=PropertyType.CHECKBOX, frozen=True
    )
    checkbox: dict = Field(default_factory=dict, frozen=True)


class CreatedByProperty(_BaseProperty):
    type: Literal[PropertyType.CREATED_BY] = Field(
        default=PropertyType.CREATED_BY, frozen=True
    )
    created_by: dict = Field(default_factory=dict, frozen=True)


class CreatedTimeProperty(_BaseProperty):
    type: Literal[PropertyType.CREATED_TIME] = Field(
        default=PropertyType.CREATED_TIME, frozen=True
    )
    created_time: dict = Field(default_factory=dict, frozen=True)


class DateProperty(_BaseProperty):
    type: Literal[PropertyType.DATE] = Field(default=PropertyType.DATE, frozen=True)
    date: dict = Field(default_factory=dict, frozen=True)


class EmailProperty(_BaseProperty):
    type: Literal[PropertyType.EMAIL] = Field(default=PropertyType.EMAIL, frozen=True)
    email: dict = Field(default_factory=dict, frozen=True)


class FilesProperty(_BaseProperty):
    type: Literal[PropertyType.FILES] = Field(default=PropertyType.FILES, frozen=True)
    files: dict = Field(default_factory=dict, frozen=True)


class FormulaProperty(_BaseProperty):
    type: Literal[PropertyType.FORMULA] = Field(
        default=PropertyType.FORMULA, frozen=True
    )
    formula: NotionEquation


class LastEditedByProperty(_BaseProperty):
    type: Literal[PropertyType.LAST_EDITED_BY] = Field(
        default=PropertyType.LAST_EDITED_BY, frozen=True
    )
    last_edited_by: dict = Field(default_factory=dict, frozen=True)


class LastEditedTimeProperty(_BaseProperty):
    type: Literal[PropertyType.LAST_EDITED_TIME] = Field(
        default=PropertyType.LAST_EDITED_TIME, frozen=True
    )
    last_edited_time: dict = Field(default_factory=dict, frozen=True)


class MultiSelectProperty(_BaseProperty):
    type: Literal[PropertyType.MULTI_SELECT] = Field(
        default=PropertyType.MULTI_SELECT, frozen=True
    )
    multi_select: SelectOptions


class NumberProperty(_BaseProperty):
    type: Literal[PropertyType.NUMBER] = Field(default=PropertyType.NUMBER, frozen=True)
    number: Number


class PeopleProperty(_BaseProperty):
    type: Literal[PropertyType.PEOPLE] = Field(default=PropertyType.PEOPLE, frozen=True)
    people: dict = Field(default_factory=dict, frozen=True)


class PhoneNumberProperty(_BaseProperty):
    type: Literal[PropertyType.PHONE_NUMBER] = Field(
        default=PropertyType.PHONE_NUMBER, frozen=True
    )
    phone_number: dict = Field(default_factory=dict, frozen=True)


class RelationProperty(_BaseProperty):
    type: Literal[PropertyType.RELATION] = Field(
        default=PropertyType.RELATION, frozen=True
    )
    relation: Relation


class RichTextProperty(_BaseProperty):
    type: Literal[PropertyType.RICH_TEXT] = Field(
        default=PropertyType.RICH_TEXT, frozen=True
    )
    rich_text: dict = Field(default_factory=dict, frozen=True)


class RollupProperty(_BaseProperty):
    type: Literal[PropertyType.ROLLUP] = Field(default=PropertyType.ROLLUP, frozen=True)
    rollup: Rollup


class SelectProperty(_BaseProperty):
    type: Literal[PropertyType.SELECT] = Field(default=PropertyType.SELECT, frozen=True)
    select: SelectOptions


class StatusProperty(_BaseProperty):
    type: Literal[PropertyType.STATUS] = Field(default=PropertyType.STATUS, frozen=True)
    status: StatusOptions
    groups: Optional[list[GroupOption]] = Field(default=None, frozen=True)


class TitleProperty(_BaseProperty):
    type: Literal[PropertyType.TITLE] = Field(default=PropertyType.TITLE, frozen=True)
    title: dict = Field(default_factory=dict, frozen=True)


class UrlProperty(_BaseProperty):
    type: Literal[PropertyType.URL] = Field(default=PropertyType.URL, frozen=True)
    url: dict = Field(default_factory=dict, frozen=True)


Property = Annotated[
    CheckboxProperty
    | CreatedByProperty
    | CreatedTimeProperty
    | DateProperty
    | EmailProperty
    | FilesProperty
    | FormulaProperty
    | LastEditedByProperty
    | LastEditedTimeProperty
    | MultiSelectProperty
    | NumberProperty
    | PeopleProperty
    | PhoneNumberProperty
    | RelationProperty
    | RichTextProperty
    | RollupProperty
    | SelectProperty
    | StatusProperty
    | TitleProperty
    | UrlProperty,
    Field(discriminator="type"),
]


class StringFormulaValue(BaseNotionModel):
    type: Literal[FormulaValueType.STRING] = Field(
        default=FormulaValueType.STRING, frozen=True
    )
    string: Optional[str] = Field(default=None)


class NumberFormulaValue(BaseNotionModel):
    type: Literal[FormulaValueType.NUMBER] = Field(
        default=FormulaValueType.NUMBER, frozen=True
    )
    number: Optional[float | int] = Field(default=None)


class BooleanFormulaValue(BaseNotionModel):
    type: Literal[FormulaValueType.BOOLEAN] = Field(
        default=FormulaValueType.BOOLEAN, frozen=True
    )
    boolean: bool


class DateFormulaValue(BaseNotionModel):
    type: Literal[FormulaValueType.DATE] = Field(
        default=FormulaValueType.DATE, frozen=True
    )
    date: Optional[NotionDate] = Field(default=None)


FormulaValue = Annotated[
    StringFormulaValue | NumberFormulaValue | BooleanFormulaValue | DateFormulaValue,
    Field(discriminator="type"),
]


class FullOptionValue(BaseNotionModel):
    id: str
    name: str
    color: Optional[Color] = Field(default=None)


class IdOnlyOptionValue(BaseNotionModel):
    id: str


class NameOnlyOptionValue(BaseNotionModel):
    name: str


def option_value_discriminator(value):
    def get_value(key: str):
        if isinstance(value, dict):
            return value.get(key, None)
        else:
            return getattr(value, key, None)

    option_id = get_value("id")
    option_name = get_value("name")

    if option_id and option_name:
        return "full"
    elif option_id:
        return "id"
    elif option_name:
        return "name"

    raise ValueError(f"Invalid option value: {value}")


OptionValue = Annotated[
    Annotated[FullOptionValue, Tag("full")]
    | Annotated[IdOnlyOptionValue, Tag("id")]
    | Annotated[NameOnlyOptionValue, Tag("name")],
    Discriminator(option_value_discriminator),
]


class ArrayRollupValue(BaseNotionModel):
    type: Literal[RollupValueType.ARRAY] = Field(
        default=RollupValueType.ARRAY, frozen=True
    )
    array: list[PropertyValue] = Field(default_factory=list)


class DateRollupValue(BaseNotionModel):
    type: Literal[RollupValueType.DATE] = Field(
        default=RollupValueType.DATE, frozen=True
    )
    date: Optional[NotionDate] = Field(default=None)


class IncompleteRollupValue(BaseNotionModel):
    type: Literal[RollupValueType.INCOMPLETE] = Field(
        default=RollupValueType.INCOMPLETE, frozen=True
    )
    incomplete: Optional[dict] = Field(default=None)


class NumberRollupValue(BaseNotionModel):
    type: Literal[RollupValueType.NUMBER] = Field(
        default=RollupValueType.NUMBER, frozen=True
    )
    number: Optional[Optional[float | int]] = Field(default=None)


class UnsupportedRollupValue(BaseNotionModel):
    type: Literal[RollupValueType.UNSUPPORTED] = Field(
        default=RollupValueType.UNSUPPORTED, frozen=True
    )
    unsupported: Optional[dict] = Field(default=None)


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
    prefix: Optional[str] = Field(default=None)


class UnverifiedValue(BaseNotionModel):
    state: Literal["unverified"]
    verified_by: None = Field(default=None)
    date: None = Field(default=None)


class VerifiedValue(BaseNotionModel):
    state: Literal["verified"]
    verified_by: User
    date: NotionDate


VerificationValue = Annotated[
    VerifiedValue | UnverifiedValue,
    Field(discriminator="state"),
]


class _BasePropertyValue(BaseNotionModel):
    id: Optional[str] = Field(default=None, frozen=True)


class CheckboxPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.CHECKBOX] = Field(
        default=PropertyType.CHECKBOX, frozen=True
    )
    checkbox: bool


class CreatedByPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.CREATED_BY] = Field(
        default=PropertyType.CREATED_BY, frozen=True
    )
    created_by: User


class CreatedTimePropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.CREATED_TIME] = Field(
        default=PropertyType.CREATED_TIME, frozen=True
    )
    created_time: Annotated[str | datetime, BeforeValidator(validate_datetime)]


class DatePropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.DATE] = Field(default=PropertyType.DATE, frozen=True)
    date: Optional[NotionDate] = Field(default=None)


class EmailPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.EMAIL] = Field(default=PropertyType.EMAIL, frozen=True)
    email: Annotated[str, BeforeValidator(validate_email)]


class FilesPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.FILES] = Field(default=PropertyType.FILES, frozen=True)
    files: list[FileWithName] = Field(default_factory=list)


class FormulaPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.FORMULA] = Field(
        default=PropertyType.FORMULA, frozen=True
    )
    formula: FormulaValue


class LastEditedByPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.LAST_EDITED_BY] = Field(
        default=PropertyType.LAST_EDITED_BY, frozen=True
    )
    last_edited_by: User


class LastEditedTimePropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.LAST_EDITED_TIME] = Field(
        default=PropertyType.LAST_EDITED_TIME, frozen=True
    )
    last_edited_time: Annotated[str | datetime, BeforeValidator(validate_datetime)]


class MultiSelectPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.MULTI_SELECT] = Field(
        default=PropertyType.MULTI_SELECT, frozen=True
    )
    multi_select: list[OptionValue] = Field(default_factory=list)


class NumberPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.NUMBER] = Field(default=PropertyType.NUMBER, frozen=True)
    number: Optional[float | int] = Field(default=None)


class PeoplePropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.PEOPLE] = Field(default=PropertyType.PEOPLE, frozen=True)
    people: list[User] = Field(default_factory=list)


class PhoneNumberPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.PHONE_NUMBER] = Field(
        default=PropertyType.PHONE_NUMBER, frozen=True
    )
    phone_number: Annotated[str, BeforeValidator(validate_phone)]


class RelationPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.RELATION] = Field(
        default=PropertyType.RELATION, frozen=True
    )
    relation: list[NotionObjectId]
    has_more: Optional[bool] = Field(default=None, frozen=True)


class RollupPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.ROLLUP] = Field(default=PropertyType.ROLLUP, frozen=True)
    rollup: RollupValue


class RichTextPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.RICH_TEXT] = Field(
        default=PropertyType.RICH_TEXT, frozen=True
    )
    rich_text: list[RichText] = Field(default_factory=list)


class SelectPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.SELECT] = Field(default=PropertyType.SELECT, frozen=True)
    select: OptionValue


class StatusPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.STATUS] = Field(default=PropertyType.STATUS, frozen=True)
    status: OptionValue


class TitlePropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.TITLE] = Field(default=PropertyType.TITLE, frozen=True)
    title: list[RichText] = Field(default_factory=list)


class UrlPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.URL] = Field(default=PropertyType.URL, frozen=True)
    url: Annotated[str, BeforeValidator(validate_url)]


class UniqueIdPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.UNIQUE_ID] = Field(
        default=PropertyType.UNIQUE_ID, frozen=True
    )
    unique_id: UniqueIdValue


class VerificationPropertyValue(_BasePropertyValue):
    type: Literal[PropertyType.VERIFICATION] = Field(
        default=PropertyType.VERIFICATION, frozen=True
    )
    verification: VerificationValue


PropertyValue = Annotated[
    CheckboxPropertyValue
    | CreatedByPropertyValue
    | CreatedTimePropertyValue
    | DatePropertyValue
    | EmailPropertyValue
    | FilesPropertyValue
    | FormulaPropertyValue
    | LastEditedByPropertyValue
    | LastEditedTimePropertyValue
    | MultiSelectPropertyValue
    | NumberPropertyValue
    | PeoplePropertyValue
    | PhoneNumberPropertyValue
    | RelationPropertyValue
    | RollupPropertyValue
    | RichTextPropertyValue
    | SelectPropertyValue
    | StatusPropertyValue
    | TitlePropertyValue
    | UrlPropertyValue
    | UniqueIdPropertyValue
    | VerificationPropertyValue,
    Field(discriminator="type"),
]
