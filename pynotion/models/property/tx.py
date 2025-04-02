from typing import Optional, Annotated, TYPE_CHECKING

from pydantic import (
    Field,
    BeforeValidator,
    Discriminator,
    Tag,
    field_validator,
    model_serializer,
)

from pynotion.models.object import NotionObjectId
from .._internal import (
    BaseNotionModel,
    validate_email,
    validate_url,
    validate_phone,
)

if TYPE_CHECKING:
    from pynotion.models.object import NotionObjectIdWrapper
    from pynotion.models.types import (
        Color,
        NotionEquation,
        NotionEmptyDict,
        NotionDate,
    )
    from pynotion.models.user import UserRef
    from pynotion.models.rich_text.tx import TxRichText
    from pynotion.models.property.types import NumberFormat, RollupFunction

__all__ = [
    # Property values
    "TxOptionValue",
    "TxCheckboxPropertyValue",
    "TxDatePropertyValue",
    "TxEmailPropertyValue",
    "TxFilesPropertyValue",
    "TxMultiSelectPropertyValue",
    "TxNumberPropertyValue",
    "TxPeoplePropertyValue",
    "TxPhoneNumberPropertyValue",
    "TxRelationPropertyValue",
    "TxRichTextPropertyValue",
    "TxSelectPropertyValue",
    "TxStatusPropertyValue",
    "TxTitlePropertyValue",
    "TxUrlPropertyValue",
    "TxPropertyValue",
    # Property schemas
    "NumberSchema",
    "DualRelationSchema",
    "SingleRelationSchema",
    "RelationSchema",
    "BaseOptionSchema",
    "SelectOptionsSchema",
    "RollupSchema",
    "TitlePropertySchema",
    "RichTextPropertySchema",
    "NumberPropertySchema",
    "SelectPropertySchema",
    "MultiSelectPropertySchema",
    "DatePropertySchema",
    "PeoplePropertySchema",
    "FilesPropertySchema",
    "CheckboxPropertySchema",
    "UrlPropertySchema",
    "EmailPropertySchema",
    "PhoneNumberPropertySchema",
    "FormulaPropertySchema",
    "RelationPropertySchema",
    "RollupPropertySchema",
    "CreatedTimePropertySchema",
    "CreatedByPropertySchema",
    "LastEditedTimePropertySchema",
    "LastEditedByPropertySchema",
    "PropertySchema",
]


class TxOptionValue(BaseNotionModel):
    """Represents an option value.

    Attributes:
        name: The name of the option.
    """

    name: str

    @field_validator("name", mode="after")
    def validate_name_field(cls, v):
        if "," in v:
            raise ValueError("Comma is not allowed in the name field")
        return v


class TxCheckboxPropertyValue(BaseNotionModel):
    """Represents a checkbox property value.

    Attributes:
        checkbox: The checkbox property value.
    """

    checkbox: bool


class TxDatePropertyValue(BaseNotionModel):
    """Represents a date property value.

    Attributes:
        date: The date property value
    """

    date: "NotionDate"


class TxEmailPropertyValue(BaseNotionModel):
    """Represents an email property value.

    Attributes:
        email: The email property value
    """

    email: Annotated[str, BeforeValidator(validate_email)]


class TxFilesPropertyValue(BaseNotionModel):
    """Represents files property value.

    Attributes:
        files: Files property value.
    """

    files: list["NotionFileWithName"] = Field(default_factory=list)


class TxMultiSelectPropertyValue(BaseNotionModel):
    """Represents a multi-select property value.

    Attributes:
        multi_select: The multi-select property value.
    """

    multi_select: list["TxOptionValue"] = Field(default_factory=list)


class TxNumberPropertyValue(BaseNotionModel):
    """Represents a number property value.

    Attributes:
        number: The number property value.
    """

    number: Optional[float | int]


class TxPeoplePropertyValue(BaseNotionModel):
    """Represents people's property value.

    Attributes:
        people: The people property value.
    """

    people: list["UserRef"] = Field(default_factory=list)


class TxPhoneNumberPropertyValue(BaseNotionModel):
    """Represents a phone number property value.

    Attributes:
        phone_number: The phone number property value.
    """

    phone_number: Annotated[str, BeforeValidator(validate_phone)]


class TxRelationPropertyValue(BaseNotionModel):
    """Represents a relation property value.

    Attributes:
        relation: The relation property value.
    """

    relation: list["NotionObjectIdWrapper"] = Field(default_factory=list)


class TxRichTextPropertyValue(BaseNotionModel):
    """Represents a rich text property value.

    Attributes:
        rich_text: The rich text property value.
    """

    rich_text: list["TxRichText"] = Field(default_factory=list)

    @model_serializer(mode="wrap")
    def _serialize_model(self, handler):
        data = handler(self)
        if "rich_text" in data:
            for item in data["rich_text"]:
                item.pop("type", None)

        return data


class TxSelectPropertyValue(BaseNotionModel):
    """Represents a select property value.

    Attributes:
        select: The select property value.
    """

    select: "TxOptionValue"


class TxStatusPropertyValue(BaseNotionModel):
    """Represents a status property value.

    Attributes:
        status: The status property value.
    """

    status: "TxOptionValue"


class TxTitlePropertyValue(BaseNotionModel):
    """Represents a title property value.

    Attributes:
        title: The title property value.
    """

    title: list["TxRichText"] = Field(default_factory=list)

    @model_serializer(mode="wrap")
    def _serialize_model(self, handler):
        data = handler(self, handler)
        if "title" in data:
            for item in data["title"]:
                item.pop("type", None)

        return data


class TxUrlPropertyValue(BaseNotionModel):
    """Represents a URL property value.

    Attributes:
        url: The URL property value.
    """

    url: Annotated[str, BeforeValidator(validate_url)]


TxPropertyValue = "TxCheckboxPropertyValue | TxDatePropertyValue | TxEmailPropertyValue | TxFilesPropertyValue | TxMultiSelectPropertyValue | TxNumberPropertyValue | TxPeoplePropertyValue | TxPhoneNumberPropertyValue | TxRelationPropertyValue | TxRichTextPropertyValue | TxSelectPropertyValue | TxStatusPropertyValue | TxTitlePropertyValue | TxUrlPropertyValue"


class NumberSchema(BaseNotionModel):
    """Represents a number property schema.

    Attributes:
        format: The format of the number property
    """

    format: "NumberFormat"


class DualRelationSchema(BaseNotionModel):
    """Represents a dual relation property schema.

    Attributes:
        database_id: The ID of the database.
        dual_property: Empty dict.
    """

    database_id: NotionObjectId
    dual_property: "NotionEmptyDict" = Field(default_factory=dict)


class SingleRelationSchema(BaseNotionModel):
    """Represents a single relation property schema.

    Attributes:
        database_id: The ID of the database.
        single_property: Empty dict.
    """

    database_id: NotionObjectId
    single_property: "NotionEmptyDict" = Field(default_factory=dict)


def model_relation_schema_discriminator(values):
    from .._internal.utils import get_value_for_discriminator

    dual_property = get_value_for_discriminator(values, "dual_property")
    if dual_property is not None:
        return "dual"
    else:
        return "single"


RelationSchema = Annotated[
    Annotated["SingleRelationSchema", Tag("single")]
    | Annotated["DualRelationSchema", Tag("dual")],
    Discriminator(model_relation_schema_discriminator),
]


class BaseOptionSchema(BaseNotionModel):
    """Represents a base option schema.

    Attributes:
        name: The name of the option.
        color: The color of the option
    """

    name: str
    color: Optional["Color"] = None


class SelectOptionsSchema(BaseNotionModel):
    """Represents the options in a select property.

    Attributes:
        options: The options in the select property
    """

    options: list["BaseOptionSchema"] = Field(default_factory=list)


class RollupSchema(BaseNotionModel):
    """Represents a rollup property schema.

    Attributes:
        relation_property_name: The name of the relation property.
        rollup_property_name: The name of the rollup property.
        function: The function of the rollup property
    """

    relation_property_name: str
    rollup_property_name: str
    function: "RollupFunction"


class TitlePropertySchema(BaseNotionModel):
    """Represents a title property schema.

    Attributes:
        title: Empty dict
    """

    title: "NotionEmptyDict" = Field(default_factory=dict)


class RichTextPropertySchema(BaseNotionModel):
    """Represents a rich text property schema.

    Attributes:
        rich_text: Empty dict
    """

    rich_text: "NotionEmptyDict" = Field(default_factory=dict)


class NumberPropertySchema(BaseNotionModel):
    """Represents a number property schema.

    Attributes:
        number: The number format
    """

    number: "NumberSchema"


class SelectPropertySchema(BaseNotionModel):
    """Represents a select property schema.

    Attributes:
        select: The options in the select property
    """

    select: "SelectOptionsSchema"


class MultiSelectPropertySchema(BaseNotionModel):
    """Represents a multi-select property schema.

    Attributes:
        multi_select: The options in the multi-select property
    """

    multi_select: "SelectOptionsSchema"


class DatePropertySchema(BaseNotionModel):
    """Represents a date property schema.

    Attributes:
        date: Empty dict
    """

    date: "NotionEmptyDict" = Field(default_factory=dict)


class PeoplePropertySchema(BaseNotionModel):
    """Represents a people property schema.

    Attributes:
        people: Empty dict
    """

    people: "NotionEmptyDict" = Field(default_factory=dict)


class FilesPropertySchema(BaseNotionModel):
    """Represents files property schema.

    Attributes:
        files: Empty dict
    """

    files: "NotionEmptyDict" = Field(default_factory=dict)


class CheckboxPropertySchema(BaseNotionModel):
    """Represents a checkbox property schema.

    Attributes:
        checkbox: Empty dict
    """

    checkbox: "NotionEmptyDict" = Field(default_factory=dict)


class UrlPropertySchema(BaseNotionModel):
    """Represents a URL property schema.

    Attributes:
        url: Empty dict
    """

    url: "NotionEmptyDict" = Field(default_factory=dict)


class EmailPropertySchema(BaseNotionModel):
    """Represents an email property schema.

    Attributes:
        email: Empty dict
    """

    email: "NotionEmptyDict" = Field(default_factory=dict)


class PhoneNumberPropertySchema(BaseNotionModel):
    """Represents a phone number property schema.

    Attributes:
        phone_number: Empty dict
    """

    phone_number: "NotionEmptyDict" = Field(default_factory=dict)


class FormulaPropertySchema(BaseNotionModel):
    """Represents a formula property schema.

    Attributes:
        formula: The formula
    """

    formula: "NotionEquation"


class RelationPropertySchema(BaseNotionModel):
    """Represents a relation property schema.

    Attributes:
        relation: The relation
    """

    relation: "RelationSchema"


class RollupPropertySchema(BaseNotionModel):
    """Represents a rollup property schema.

    Attributes:
        rollup: The rollup
    """

    rollup: "RollupSchema"


class CreatedTimePropertySchema(BaseNotionModel):
    """Represents a created time property schema.

    Attributes:
        created_time: Empty dict
    """

    created_time: "NotionEmptyDict" = Field(default_factory=dict)


class CreatedByPropertySchema(BaseNotionModel):
    """Represents a created by property schema.

    Attributes:
        created_by: Empty dict
    """

    created_by: "NotionEmptyDict" = Field(default_factory=dict)


class LastEditedTimePropertySchema(BaseNotionModel):
    """Represents a last edited time property schema.

    Attributes:
        last_edited_time: Empty dict
    """

    last_edited_time: "NotionEmptyDict" = Field(default_factory=dict)


class LastEditedByPropertySchema(BaseNotionModel):
    """Represents a last edited by property schema.

    Attributes:
        last_edited_by: Empty dict
    """

    last_edited_by: "NotionEmptyDict" = Field(default_factory=dict)


PropertySchema = "TitlePropertySchema | RichTextPropertySchema | NumberPropertySchema | SelectPropertySchema | MultiSelectPropertySchema | DatePropertySchema | PeoplePropertySchema | FilesPropertySchema | CheckboxPropertySchema | UrlPropertySchema | EmailPropertySchema | PhoneNumberPropertySchema | FormulaPropertySchema | RelationPropertySchema | RollupPropertySchema | CreatedTimePropertySchema | CreatedByPropertySchema | LastEditedTimePropertySchema | LastEditedByPropertySchema"
