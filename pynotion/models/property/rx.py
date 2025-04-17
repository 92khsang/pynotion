from typing import Literal, Optional, Annotated, TYPE_CHECKING, Union
from uuid import UUID

from pydantic import (
    BeforeValidator,
    Discriminator,
    Tag,
)

from pynotion.models.property.types import (
    NumberFormat,
    RollupFunction,
    PropertyType,
    RollupValueType,
)
from .._internal import (
    FrozenNotionModel,
    validate_email,
    validate_url,
    validate_phone,
)
from .._internal.utils import discriminate_field

if TYPE_CHECKING:
    from pynotion.models.object import NotionObjectIdWrapper
    from pynotion.models.types import (
        Color,
        NotionEquation,
        NotionEmptyDict,
        NotionDate,
        NotionDatetime,
    )
    from pynotion.models.user import NotionUser
    from pynotion.models.file import NotionFileWithName
    from pynotion.models.rich_text.rx import RxRichText
    from pynotion.models.property.common import FormulaValue

__all__ = [
    # Property Objects
    "BaseOption",
    "SelectOptions",
    "Number",
    "SyncRelation",
    "DualRelation",
    "SingleRelation",
    "Relation",
    "Rollup",
    "StatusOptions",
    "GroupOption",
    # Property
    "Property",
    "CheckboxProperty",
    "CreatedByProperty",
    "CreatedTimeProperty",
    "DateProperty",
    "EmailProperty",
    "FilesProperty",
    "FormulaProperty",
    "LastEditedByProperty",
    "LastEditedTimeProperty",
    "MultiSelectProperty",
    "NumberProperty",
    "PeopleProperty",
    "PhoneNumberProperty",
    "RelationProperty",
    "RichTextProperty",
    "RollupProperty",
    "SelectProperty",
    "StatusProperty",
    "TitleProperty",
    "UrlProperty",
    # Property Value
    "ArrayRollupValue",
    "DateRollupValue",
    "IncompleteRollupValue",
    "NumberRollupValue",
    "UnsupportedRollupValue",
    "RollupValue",
    "UniqueIdValue",
    "UnverifiedValue",
    "VerifiedValue",
    "VerificationValue",
    "RxOptionValue",
    "CreatedByPropertyValue",
    "CreatedTimePropertyValue",
    "LastEditedByPropertyValue",
    "LastEditedTimePropertyValue",
    "RollupPropertyValue",
    "FormulaPropertyValue",
    "UniqueIdPropertyValue",
    "VerificationPropertyValue",
    "RxCheckboxPropertyValue",
    "RxDatePropertyValue",
    "RxEmailPropertyValue",
    "RxFilesPropertyValue",
    "RxMultiSelectPropertyValue",
    "RxNumberPropertyValue",
    "RxPeoplePropertyValue",
    "RxPhoneNumberPropertyValue",
    "RxRelationPropertyValue",
    "RxRichTextPropertyValue",
    "RxSelectPropertyValue",
    "RxStatusPropertyValue",
    "RxTitlePropertyValue",
    "RxUrlPropertyValue",
    "RxPropertyValue",
    # Property Item
    "RxPaginatedTitlePropertyItem",
    "RxPaginatedRichTextPropertyItem",
    "RxPaginatedRelationPropertyItem",
    "RxPaginatedPeoplePropertyItem",
    "RxPaginatedPropertyItem",
    "RxTitlePropertyItem",
    "RxRichTextPropertyItem",
    "RxRelationPropertyItem",
    "RxPeoplePropertyItem",
    "RxRollupPropertyItem",
    "RxPropertyItem",
    # Class Map
    "PROPERTY_CLASS_MAP",
    "ROLLUP_VALUE_CLASS_MAP",
    "VERIFICATION_VALUE_CLASS_MAP",
    "RX_PROPERTY_VALUE_CLASS_MAP",
    "RX_PAGINATED_PROPERTY_ITEM_CLASS_MAP",
    "RX_PROPERTY_ITEM_CLASS_MAP",
]


class BaseOption(FrozenNotionModel):
    """Represents an option in a select property.

    Attributes:
        id: The ID of the option.
        name: The name of the option.
        color: The color of the option.
    """

    id: str
    name: str
    color: "Color"


class SelectOptions(FrozenNotionModel):
    """Represents the options in a select property.

    Attributes:
        options: The options in the select property.
    """

    options: list["BaseOption"]


class Number(FrozenNotionModel):
    """Represents a number property.

    Attributes:
        format: The format of the number property.
    """

    format: "NumberFormat"


class SyncRelation(FrozenNotionModel):
    """Represents a synced relation.

    Attributes:
        synced_property_id: The ID of the synced property.
        synced_property_name: The name of the synced property.
    """

    synced_property_id: Optional[str] = None
    synced_property_name: Optional[str] = None


class DualRelation(FrozenNotionModel):
    """Represents a dual relation.

    Attributes:
        database_id: The ID of the database.
        dual_property: The synced property.
    """

    database_id: UUID
    dual_property: "SyncRelation"


class SingleRelation(FrozenNotionModel):
    """Represents a single relation.

    Attributes:
        database_id: The ID of the database.
        single_property: The synced property.
    """

    database_id: UUID
    single_property: "SyncRelation"


def model_relation_discriminator(values):
    from .._internal.utils import get_value_for_discriminator

    dual_property = get_value_for_discriminator(values, "dual_property")
    if dual_property:
        return "DualRelation"
    else:
        return "SingleRelation"


Relation = Annotated[
    Annotated["SingleRelation", Tag("SingleRelation")]
    | Annotated["DualRelation", Tag("DualRelation")],
    Discriminator(model_relation_discriminator),
]


class Rollup(FrozenNotionModel):
    """Represents a rollup property.

    Attributes:
        relation_property_id: The ID of the relation property.
        rollup_property_id: The ID of the rollup property.
        relation_property_name: The name of the relation property.
        rollup_property_name: The name of the rollup property.
        function: The function of the rollup property.
    """

    relation_property_id: str
    rollup_property_id: str
    relation_property_name: str
    rollup_property_name: str
    function: "RollupFunction"


class StatusOptions(FrozenNotionModel):
    """Represents the options in a status property.

    Attributes:
        options: The options in the status property.
    """

    options: list["BaseOption"]


class GroupOption(FrozenNotionModel):
    """Represents a group option in a status property.

    Attributes:
        option_ids: The IDs of the options in the group.
    """

    option_ids: list[UUID]


class _BaseProperty(FrozenNotionModel):
    """Represents a base property.

    Attributes:
        id: The ID of the property.
        name: The name of the property.
    """

    id: str
    name: str


class CheckboxProperty(_BaseProperty):
    """Represents a checkbox property.

    Attributes:
        type: The type of the property.
        checkbox: Empty dict.
    """

    type: Literal[PropertyType.CHECKBOX] = PropertyType.CHECKBOX
    checkbox: "NotionEmptyDict"


class CreatedByProperty(_BaseProperty):
    """Represents a created by property.

    Attributes:
        type: The type of the property.
        created_by: Empty dict.
    """

    type: Literal[PropertyType.CREATED_BY] = PropertyType.CREATED_BY
    created_by: "NotionEmptyDict"


class CreatedTimeProperty(_BaseProperty):
    """Represents a created time property.

    Attributes:
        type: The type of the property.
        created_time: Empty dict.
    """

    type: Literal[PropertyType.CREATED_TIME] = PropertyType.CREATED_TIME
    created_time: "NotionEmptyDict"


class DateProperty(_BaseProperty):
    """Represents a date property.

    Attributes:
        type: The type of the property.
        date: Empty dict.
    """

    type: Literal[PropertyType.DATE] = PropertyType.DATE
    date: "NotionEmptyDict"


class EmailProperty(_BaseProperty):
    """Represents an email property.

    Attributes:
        type: The type of the property.
        email: Empty dict.
    """

    type: Literal[PropertyType.EMAIL] = PropertyType.EMAIL
    email: "NotionEmptyDict"


class FilesProperty(_BaseProperty):
    """Represents files property.

    Attributes:
        type: The type of the property.
        files: Empty dict.
    """

    type: Literal[PropertyType.FILES] = PropertyType.FILES
    files: "NotionEmptyDict"


class FormulaProperty(_BaseProperty):
    """Represents a formula property.

    Attributes:
        type: The type of the property.
        formula: The formula equation.
    """

    type: Literal[PropertyType.FORMULA] = PropertyType.FORMULA
    formula: "NotionEquation"


class LastEditedByProperty(_BaseProperty):
    """Represents a last edited by property.

    Attributes:
        type: The type of the property.
        last_edited_by: Empty dict
    """

    type: Literal[PropertyType.LAST_EDITED_BY] = PropertyType.LAST_EDITED_BY
    last_edited_by: "NotionEmptyDict"


class LastEditedTimeProperty(_BaseProperty):
    """Represents a last edited time property.

    Attributes:
        type: The type of the property.
        last_edited_time: Empty dict
    """

    type: Literal[PropertyType.LAST_EDITED_TIME] = PropertyType.LAST_EDITED_TIME
    last_edited_time: "NotionEmptyDict"


class MultiSelectProperty(_BaseProperty):
    """Represents a multi-select property.

    Attributes:
        type: The type of the property.
        multi_select: The options for the multi-select property.
    """

    type: Literal[PropertyType.MULTI_SELECT] = PropertyType.MULTI_SELECT
    multi_select: "SelectOptions"


class NumberProperty(_BaseProperty):
    """Represents a number property.

    Attributes:
        type: The type of the property.
        number: The number format.
    """

    type: Literal[PropertyType.NUMBER] = PropertyType.NUMBER
    number: "Number"


class PeopleProperty(_BaseProperty):
    """Represents a "people" property.

    Attributes:
        type: The type of the property.
        people: Empty dict
    """

    type: Literal[PropertyType.PEOPLE] = PropertyType.PEOPLE
    people: "NotionEmptyDict"


class PhoneNumberProperty(_BaseProperty):
    """Represents a phone number property.

    Attributes:
        type: The type of the property.
        phone_number: Empty dict
    """

    type: Literal[PropertyType.PHONE_NUMBER] = PropertyType.PHONE_NUMBER
    phone_number: "NotionEmptyDict"


class RelationProperty(_BaseProperty):
    """Represents a relation property.

    Attributes:
        type: The type of the property.
        relation: The single relation or dual relation.
    """

    type: Literal[PropertyType.RELATION] = PropertyType.RELATION
    relation: "Relation"


class RichTextProperty(_BaseProperty):
    """Represents a rich text property.

    Attributes:
        type: The type of the property.
        rich_text: Empty dict
    """

    type: Literal[PropertyType.RICH_TEXT] = PropertyType.RICH_TEXT
    rich_text: "NotionEmptyDict"


class RollupProperty(_BaseProperty):
    """Represents a rollup property.

    Attributes:
        type: The type of the property.
        rollup: The rollup property.
    """

    type: Literal[PropertyType.ROLLUP] = PropertyType.ROLLUP
    rollup: "Rollup"


class SelectProperty(_BaseProperty):
    """Represents a select property.

    Attributes:
        type: The type of the property.
        select: The options for the select property.
    """

    type: Literal[PropertyType.SELECT] = PropertyType.SELECT
    select: "SelectOptions"


class StatusProperty(_BaseProperty):
    """Represents a status property.

    Attributes:
        type: The type of the property.
        status: The options for the status property.
        groups: The groups for the status property.
    """

    type: Literal[PropertyType.STATUS] = PropertyType.STATUS
    status: "StatusOptions"
    groups: Optional[list["GroupOption"]] = None


class TitleProperty(_BaseProperty):
    """Represents a title property.

    Attributes:
        type: The type of the property.
        title: Empty dict
    """

    type: Literal[PropertyType.TITLE] = PropertyType.TITLE
    title: "NotionEmptyDict"


class UrlProperty(_BaseProperty):
    """represents url property.

    Attributes:
        type: The type of the property.
        url: Empty dict
    """

    type: Literal[PropertyType.URL] = PropertyType.URL
    url: "NotionEmptyDict"


PROPERTY_CLASS_MAP = {
    PropertyType.CHECKBOX: "CheckboxProperty",
    PropertyType.CREATED_BY: "CreatedByProperty",
    PropertyType.CREATED_TIME: "CreatedTimeProperty",
    PropertyType.DATE: "DateProperty",
    PropertyType.EMAIL: "EmailProperty",
    PropertyType.FILES: "FilesProperty",
    PropertyType.FORMULA: "FormulaProperty",
    PropertyType.LAST_EDITED_BY: "LastEditedByProperty",
    PropertyType.LAST_EDITED_TIME: "LastEditedTimeProperty",
    PropertyType.MULTI_SELECT: "MultiSelectProperty",
    PropertyType.NUMBER: "NumberProperty",
    PropertyType.PEOPLE: "PeopleProperty",
    PropertyType.PHONE_NUMBER: "PhoneNumberProperty",
    PropertyType.RELATION: "RelationProperty",
    PropertyType.RICH_TEXT: "RichTextProperty",
    PropertyType.ROLLUP: "RollupProperty",
    PropertyType.SELECT: "SelectProperty",
    PropertyType.STATUS: "StatusProperty",
    PropertyType.TITLE: "TitleProperty",
    PropertyType.URL: "UrlProperty",
}

if not TYPE_CHECKING:
    Property = Annotated[
        Union[tuple(PROPERTY_CLASS_MAP.values())],
        BeforeValidator(lambda v: discriminate_field(v, "type", PROPERTY_CLASS_MAP)),
    ]
else:
    Property = Union[
        CheckboxProperty,
        CreatedByProperty,
        CreatedTimeProperty,
        DateProperty,
        EmailProperty,
        FilesProperty,
        FormulaProperty,
        LastEditedByProperty,
        LastEditedTimeProperty,
        MultiSelectProperty,
        NumberProperty,
        PeopleProperty,
        PhoneNumberProperty,
        RelationProperty,
        RichTextProperty,
        RollupProperty,
        SelectProperty,
        StatusProperty,
        TitleProperty,
        UrlProperty,
    ]


class ArrayRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.ARRAY] = RollupValueType.ARRAY
    array: Optional[list["RxPropertyValue"]] = None
    function: "RollupFunction"


class DateRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.DATE] = RollupValueType.DATE
    date: Optional["NotionDate"] = None
    function: "RollupFunction"


class IncompleteRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.INCOMPLETE] = RollupValueType.INCOMPLETE
    incomplete: Optional["dict"] = None
    function: "RollupFunction"


class NumberRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.NUMBER] = RollupValueType.NUMBER
    number: Optional[float | int] = None
    function: "RollupFunction"


class UnsupportedRollupValue(FrozenNotionModel):
    type: Literal[RollupValueType.UNSUPPORTED] = RollupValueType.UNSUPPORTED
    unsupported: Optional["dict"] = None
    function: "RollupFunction"


ROLLUP_VALUE_CLASS_MAP = {
    RollupValueType.ARRAY: "ArrayRollupValue",
    RollupValueType.DATE: "DateRollupValue",
    RollupValueType.INCOMPLETE: "IncompleteRollupValue",
    RollupValueType.NUMBER: "NumberRollupValue",
    RollupValueType.UNSUPPORTED: "UnsupportedRollupValue",
}

RollupValue = Annotated[
    Union[tuple(ROLLUP_VALUE_CLASS_MAP.values())],
    BeforeValidator(lambda v: discriminate_field(v, "type", ROLLUP_VALUE_CLASS_MAP)),
]


class UniqueIdValue(FrozenNotionModel):
    """Represents a unique id value.

    Attributes:
        number: The number of the unique id.
        prefix: The prefix of the unique id.
    """

    number: int
    prefix: Optional["str"] = None


class UnverifiedValue(FrozenNotionModel):
    """Represents an unverified value.

    Attributes:
        state: The state of the value.
        verified_by: None.
        date: None
    """

    state: Literal["unverified"] = "unverified"
    verified_by: None = None
    date: None = None


class VerifiedValue(FrozenNotionModel):
    """Represents a verified value.

    Attributes:
        state: The state of the value.
        verified_by: The user who verified the value.
        date: The date when the value was verified.
    """

    state: Literal["verified"] = "verified"
    verified_by: "NotionUser"
    date: "NotionDate"


VERIFICATION_VALUE_CLASS_MAP = {
    "unverified": "UnverifiedValue",
    "verified": "VerifiedValue",
}

VerificationValue = Annotated[
    Union[tuple(VERIFICATION_VALUE_CLASS_MAP.values())],
    BeforeValidator(
        lambda v: discriminate_field(v, "state", VERIFICATION_VALUE_CLASS_MAP)
    ),
]


class RxOptionValue(FrozenNotionModel):
    """Represents an option value.

    Attributes:
        id: The id of the option.
        name: The name of the option.
        color: The color of the option.
    """

    id: str
    name: str
    color: "Color"


class _RxBasePropertyValue(FrozenNotionModel):
    """Represents a base property value.

    Attributes:
        id: The id of the property value.
    """

    id: str


class CreatedByPropertyValue(_RxBasePropertyValue):
    """Represents a created by property value.

    Attributes:
        type: The type of the property value.
        created_by: The user who created the property value.
    """

    type: Literal[PropertyType.CREATED_BY] = PropertyType.CREATED_BY
    created_by: "NotionUser"


class CreatedTimePropertyValue(_RxBasePropertyValue):
    """Represents a created time property value.

    Attributes:
        type: The type of the property value.
        created_time: The date and time when the property value was created.
    """

    type: Literal[PropertyType.CREATED_TIME] = PropertyType.CREATED_TIME
    created_time: "NotionDatetime"


class LastEditedByPropertyValue(_RxBasePropertyValue):
    """Represents a last edited by property value.

    Attributes:
        type: The type of the property value.
        last_edited_by: The user who last edited the property value.
    """

    type: Literal[PropertyType.LAST_EDITED_BY] = PropertyType.LAST_EDITED_BY
    last_edited_by: "NotionUser"


class LastEditedTimePropertyValue(_RxBasePropertyValue):
    """Represents a last edited time property value.

    Attributes:
        type: The type of the property value.
        last_edited_time: The date and time when the property value was last edited.
    """

    type: Literal[PropertyType.LAST_EDITED_TIME] = PropertyType.LAST_EDITED_TIME
    last_edited_time: "NotionDatetime"


class RollupPropertyValue(_RxBasePropertyValue):
    """Represents a rollup property value.

    Attributes:
        type: The type of the property value.
        rollup: The rollup property value.
    """

    type: Literal[PropertyType.ROLLUP] = PropertyType.ROLLUP
    rollup: "RollupValue"


class FormulaPropertyValue(_RxBasePropertyValue):
    """Represents a formula property value.

    Attributes:
        type: The type of the property value.
        formula: The formula property value.
    """

    type: Literal[PropertyType.FORMULA] = PropertyType.FORMULA
    formula: "FormulaValue"


class UniqueIdPropertyValue(_RxBasePropertyValue):
    """Represents a unique id property value.

    Attributes:
        type: The type of the property value.
        unique_id: The unique id property value.
    """

    type: Literal[PropertyType.UNIQUE_ID] = PropertyType.UNIQUE_ID
    unique_id: "UniqueIdValue"


class VerificationPropertyValue(_RxBasePropertyValue):
    """Represents a verification property value.

    Attributes:
        type: The type of the property value.
        verification: The verification property value.
    """

    type: Literal[PropertyType.VERIFICATION] = PropertyType.VERIFICATION
    verification: "VerificationValue"


class RxCheckboxPropertyValue(_RxBasePropertyValue):
    """Represents a checkbox property value.

    Attributes:
        type: The type of the property value.
        checkbox: The checkbox property value.
    """

    type: Literal[PropertyType.CHECKBOX] = PropertyType.CHECKBOX
    checkbox: bool


class RxDatePropertyValue(_RxBasePropertyValue):
    """Represents a date property value.

    Attributes:
        type: The type of the property value.
        date: The date property value.
    """

    type: Literal[PropertyType.DATE] = PropertyType.DATE
    date: Optional["NotionDate"] = None


class RxEmailPropertyValue(_RxBasePropertyValue):
    """Represents an email property value.

    Attributes:
        type: The type of the property value.
        email: The email property value.
    """

    type: Literal[PropertyType.EMAIL] = PropertyType.EMAIL
    email: Optional[Annotated[str, BeforeValidator(validate_email)]] = None


class RxFilesPropertyValue(_RxBasePropertyValue):
    """Represents a "files" property value.

    Attributes:
        type: The type of the property value.
        files: The files property value.
    """

    type: Literal[PropertyType.FILES] = PropertyType.FILES
    files: list["NotionFileWithName"]


class RxMultiSelectPropertyValue(_RxBasePropertyValue):
    """Represents a multi-select property value.

    Attributes:
        type: The type of the property value.
        multi_select: The multi-select property value.
    """

    type: Literal[PropertyType.MULTI_SELECT] = PropertyType.MULTI_SELECT
    multi_select: list["RxOptionValue"]


class RxNumberPropertyValue(_RxBasePropertyValue):
    """Represents a number property value.

    Attributes:
        type: The type of the property value.
        number: The number property value.
    """

    type: Literal[PropertyType.NUMBER] = PropertyType.NUMBER
    number: Optional[float | int] = None


class RxPeoplePropertyValue(_RxBasePropertyValue):
    """Represents 'people' property value.

    Attributes:
        type: The type of the property value.
        people: The people property value.
    """

    type: Literal[PropertyType.PEOPLE] = PropertyType.PEOPLE
    people: list["NotionUser"]


class RxPhoneNumberPropertyValue(_RxBasePropertyValue):
    """Represents a phone number property value.

    Attributes:
        type: The type of the property value.
        phone_number: The phone number property value.
    """

    type: Literal[PropertyType.PHONE_NUMBER] = PropertyType.PHONE_NUMBER
    phone_number: Optional[Annotated[str, BeforeValidator(validate_phone)]] = None


class RxRelationPropertyValue(_RxBasePropertyValue):
    """Represents a relation property value.

    Attributes:
        type: The type of the property value.
        relation: The relation property value.
        has_more: Whether there are more relations.
    """

    type: Literal[PropertyType.RELATION] = PropertyType.RELATION
    relation: list["NotionObjectIdWrapper"]
    has_more: bool


class RxRichTextPropertyValue(_RxBasePropertyValue):
    """Represents a rich text property value.

    Attributes:
        type: The type of the property value.
        rich_text: The rich text property value.
    """

    type: Literal[PropertyType.RICH_TEXT] = PropertyType.RICH_TEXT
    rich_text: list["RxRichText"]


class RxSelectPropertyValue(_RxBasePropertyValue):
    """Represents a select property value.

    Attributes:
        type: The type of the property value.
        select: The select property value.
    """

    type: Literal[PropertyType.SELECT] = PropertyType.SELECT
    select: Optional["RxOptionValue"] = None


class RxStatusPropertyValue(_RxBasePropertyValue):
    """Represents a status property value.

    Attributes:
        type: The type of the property value.
        status: The status property value.
    """

    type: Literal[PropertyType.STATUS] = PropertyType.STATUS
    status: Optional["RxOptionValue"] = None


class RxTitlePropertyValue(_RxBasePropertyValue):
    """Represents a title property value.

    Attributes:
        type: The type of the property value.
        title: The title property value.
    """

    type: Literal[PropertyType.TITLE] = PropertyType.TITLE
    title: list["RxRichText"]


class RxUrlPropertyValue(_RxBasePropertyValue):
    """Represents a URL property value.

    Attributes:
        type: The type of the property value.
        url: The URL property value.
    """

    type: Literal[PropertyType.URL] = PropertyType.URL
    url: Optional[Annotated[str, BeforeValidator(validate_url)]] = None


RX_PROPERTY_VALUE_CLASS_MAP = {
    PropertyType.CHECKBOX: "RxCheckboxPropertyValue",
    PropertyType.CREATED_BY: "CreatedByPropertyValue",
    PropertyType.CREATED_TIME: "CreatedTimePropertyValue",
    PropertyType.DATE: "RxDatePropertyValue",
    PropertyType.EMAIL: "RxEmailPropertyValue",
    PropertyType.FILES: "RxFilesPropertyValue",
    PropertyType.FORMULA: "FormulaPropertyValue",
    PropertyType.LAST_EDITED_BY: "LastEditedByPropertyValue",
    PropertyType.LAST_EDITED_TIME: "LastEditedTimePropertyValue",
    PropertyType.MULTI_SELECT: "RxMultiSelectPropertyValue",
    PropertyType.NUMBER: "RxNumberPropertyValue",
    PropertyType.PEOPLE: "RxPeoplePropertyValue",
    PropertyType.PHONE_NUMBER: "RxPhoneNumberPropertyValue",
    PropertyType.RELATION: "RxRelationPropertyValue",
    PropertyType.RICH_TEXT: "RxRichTextPropertyValue",
    PropertyType.ROLLUP: "RollupPropertyValue",
    PropertyType.SELECT: "RxSelectPropertyValue",
    PropertyType.STATUS: "RxStatusPropertyValue",
    PropertyType.TITLE: "RxTitlePropertyValue",
    PropertyType.URL: "RxUrlPropertyValue",
    PropertyType.UNIQUE_ID: "UniqueIdPropertyValue",
    PropertyType.VERIFICATION: "VerificationPropertyValue",
}

if not TYPE_CHECKING:
    RxPropertyValue = Annotated[
        Union[tuple(RX_PROPERTY_VALUE_CLASS_MAP.values())],
        BeforeValidator(
            lambda v: discriminate_field(v, "type", RX_PROPERTY_VALUE_CLASS_MAP)
        ),
    ]
else:
    RxPropertyValue = Union[
        RxCheckboxPropertyValue,
        CreatedByPropertyValue,
        CreatedTimePropertyValue,
        RxDatePropertyValue,
        RxEmailPropertyValue,
        RxFilesPropertyValue,
        FormulaPropertyValue,
        LastEditedByPropertyValue,
        LastEditedTimePropertyValue,
        RxMultiSelectPropertyValue,
        RxNumberPropertyValue,
        RxPeoplePropertyValue,
        RxPhoneNumberPropertyValue,
        RxRelationPropertyValue,
        RxRichTextPropertyValue,
        RollupPropertyValue,
        RxSelectPropertyValue,
        RxStatusPropertyValue,
        RxTitlePropertyValue,
        RxUrlPropertyValue,
        UniqueIdPropertyValue,
        VerificationPropertyValue,
    ]


class RxPaginatedTitlePropertyItem(_RxBasePropertyValue):
    """Represents a paginated title property item.

    Attributes:
        type: The type of the property value.
        title: The title property value.
    """

    type: Literal[PropertyType.TITLE] = PropertyType.TITLE
    title: "RxRichText"


class RxPaginatedRichTextPropertyItem(_RxBasePropertyValue):
    """Represents a paginated rich text property item.

    Attributes:
        type: The type of the property value.
        rich_text: The rich text property value.
    """

    type: Literal[PropertyType.RICH_TEXT] = PropertyType.RICH_TEXT
    rich_text: "RxRichText"


class RxPaginatedRelationPropertyItem(_RxBasePropertyValue):
    """Represents a paginated relation property item.

    Attributes:
        type: The type of the property value.
        relation: The relation property value.
    """

    type: Literal[PropertyType.RELATION] = PropertyType.RELATION
    relation: "NotionObjectIdWrapper"


class RxPaginatedPeoplePropertyItem(_RxBasePropertyValue):
    """Represents a paginated people property item.

    Attributes:
        type: The type of the property value.
        people: The people property value
    """

    type: Literal[PropertyType.PEOPLE] = PropertyType.PEOPLE
    people: "NotionUser"


RX_PAGINATED_PROPERTY_ITEM_CLASS_MAP = {
    PropertyType.TITLE: "RxPaginatedTitlePropertyItem",
    PropertyType.RICH_TEXT: "RxPaginatedRichTextPropertyItem",
    PropertyType.RELATION: "RxPaginatedRelationPropertyItem",
    PropertyType.PEOPLE: "RxPaginatedPeoplePropertyItem",
}

if not TYPE_CHECKING:
    RxPaginatedPropertyItem = Annotated[
        Union[tuple(RX_PAGINATED_PROPERTY_ITEM_CLASS_MAP.values())],
        BeforeValidator(
            lambda v: discriminate_field(
                v, "type", RX_PAGINATED_PROPERTY_ITEM_CLASS_MAP
            )
        ),
    ]
else:
    RxPaginatedPropertyItem = Union[
        RxPaginatedTitlePropertyItem,
        RxPaginatedRichTextPropertyItem,
        RxPaginatedRelationPropertyItem,
        RxPaginatedPeoplePropertyItem,
    ]


class _RxBasePropertyItem(_RxBasePropertyValue):
    """Represents a base property item.

    Attributes:
        next_url: The next URL of the property item
    """

    next_url: Optional[Annotated[str, BeforeValidator(validate_url)]]


class RxTitlePropertyItem(_RxBasePropertyItem):
    """Represents a title property item.

    Attributes:
        type: The type of the property item.
        title: The title property item
    """

    type: Literal[PropertyType.TITLE] = PropertyType.TITLE
    title: dict


class RxRichTextPropertyItem(_RxBasePropertyItem):
    """Represents a rich text property item.

    Attributes:
        type: The type of the property item.
        rich_text: The rich text property item
    """

    type: Literal[PropertyType.RICH_TEXT] = PropertyType.RICH_TEXT
    rich_text: dict


class RxRelationPropertyItem(_RxBasePropertyItem):
    """Represents a relation property item.

    Attributes:
        type: The type of the property item.
        relation: The relation property item
    """

    type: Literal[PropertyType.RELATION] = PropertyType.RELATION
    relation: dict


class RxPeoplePropertyItem(_RxBasePropertyItem):
    """Represents a "people" property item.

    Attributes:
        type: The type of the property item.
        people: The people property item
    """

    type: Literal[PropertyType.PEOPLE] = PropertyType.PEOPLE
    people: dict


class RxRollupPropertyItem(_RxBasePropertyItem):
    """Represents a rollup property item.

    Attributes:
        type: The type of the property item.
        rollup: The rollup property item
    """

    type: Literal[PropertyType.ROLLUP] = PropertyType.ROLLUP
    rollup: "RollupValue"


RX_PROPERTY_ITEM_CLASS_MAP = {
    PropertyType.TITLE: "RxTitlePropertyItem",
    PropertyType.RICH_TEXT: "RxRichTextPropertyItem",
    PropertyType.RELATION: "RxRelationPropertyItem",
    PropertyType.PEOPLE: "RxPeoplePropertyItem",
    PropertyType.ROLLUP: "RxRollupPropertyItem",
}

if not TYPE_CHECKING:
    RxPropertyItem = Annotated[
        Union[tuple(RX_PROPERTY_ITEM_CLASS_MAP.values())],
        BeforeValidator(
            lambda v: discriminate_field(v, "type", RX_PROPERTY_ITEM_CLASS_MAP)
        ),
    ]
else:
    RxPropertyItem = Union[
        RxTitlePropertyItem,
        RxRichTextPropertyItem,
        RxRelationPropertyItem,
        RxPeoplePropertyItem,
        RxRollupPropertyItem,
    ]
