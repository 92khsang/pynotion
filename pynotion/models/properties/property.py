from __future__ import annotations as _annotations

from typing import Literal, Optional, Annotated
from uuid import UUID

from pydantic import (
    Field,
    BeforeValidator,
    Discriminator,
    Tag,
)

from .types import NumberFormat, RollupFunction, PropertyType
from .._internal import (
    validate_uuid4,
    FrozenNotionModel,
)
from ..object import NotionObjectId
from ..types import NotionEquation, Color, NotionEmptyDict


class BaseOption(FrozenNotionModel):
    id: str
    name: str
    color: Color


class SelectOptions(FrozenNotionModel):
    options: list[BaseOption]


class Number(FrozenNotionModel):
    format: NumberFormat


class DualProperty(FrozenNotionModel):
    synced_property_id: Optional[str]
    synced_property_name: Optional[str]


class DualRelation(FrozenNotionModel):
    database_id: NotionObjectId
    dual_property: DualProperty


class SingleRelation(FrozenNotionModel):
    database_id: NotionObjectId
    synced_property_id: Optional[str]
    synced_property_name: Optional[str]


def model_relation_discriminator(values):
    from .._internal.utils import get_value_for_discriminator

    dual_property = get_value_for_discriminator(values, "dual_property")
    if dual_property:
        return "dual"
    else:
        return "single"


Relation = Annotated[
    Annotated[SingleRelation, Tag("single")] | Annotated[DualRelation, Tag("dual")],
    Discriminator(model_relation_discriminator),
]


class Rollup(FrozenNotionModel):
    relation_property_id: str
    rollup_property_id: str
    relation_property_name: str
    rollup_property_name: str
    function: RollupFunction


class StatusOptions(FrozenNotionModel):
    options: list[BaseOption]


class GroupOption(FrozenNotionModel):
    option_ids: list[
        Annotated[str | int | bytes | UUID, BeforeValidator(validate_uuid4)]
    ]


class _BaseProperty(FrozenNotionModel):
    id: str
    name: str


class CheckboxProperty(_BaseProperty):
    type: Literal[PropertyType.CHECKBOX] = PropertyType.CHECKBOX
    checkbox: NotionEmptyDict


class CreatedByProperty(_BaseProperty):
    type: Literal[PropertyType.CREATED_BY] = PropertyType.CREATED_BY
    created_by: NotionEmptyDict


class CreatedTimeProperty(_BaseProperty):
    type: Literal[PropertyType.CREATED_TIME] = PropertyType.CREATED_TIME
    created_time: NotionEmptyDict


class DateProperty(_BaseProperty):
    type: Literal[PropertyType.DATE] = PropertyType.DATE
    date: NotionEmptyDict


class EmailProperty(_BaseProperty):
    type: Literal[PropertyType.EMAIL] = PropertyType.EMAIL
    email: NotionEmptyDict


class FilesProperty(_BaseProperty):
    type: Literal[PropertyType.FILES] = PropertyType.FILES
    files: NotionEmptyDict


class FormulaProperty(_BaseProperty):
    type: Literal[PropertyType.FORMULA] = PropertyType.FORMULA
    formula: NotionEquation


class LastEditedByProperty(_BaseProperty):
    type: Literal[PropertyType.LAST_EDITED_BY] = PropertyType.LAST_EDITED_BY
    last_edited_by: NotionEmptyDict


class LastEditedTimeProperty(_BaseProperty):
    type: Literal[PropertyType.LAST_EDITED_TIME] = PropertyType.LAST_EDITED_TIME
    last_edited_time: NotionEmptyDict


class MultiSelectProperty(_BaseProperty):
    type: Literal[PropertyType.MULTI_SELECT] = PropertyType.MULTI_SELECT
    multi_select: SelectOptions


class NumberProperty(_BaseProperty):
    type: Literal[PropertyType.NUMBER] = PropertyType.NUMBER
    number: Number


class PeopleProperty(_BaseProperty):
    type: Literal[PropertyType.PEOPLE] = PropertyType.PEOPLE
    people: NotionEmptyDict


class PhoneNumberProperty(_BaseProperty):
    type: Literal[PropertyType.PHONE_NUMBER] = PropertyType.PHONE_NUMBER
    phone_number: NotionEmptyDict


class RelationProperty(_BaseProperty):
    type: Literal[PropertyType.RELATION] = PropertyType.RELATION
    relation: Relation


class RichTextProperty(_BaseProperty):
    type: Literal[PropertyType.RICH_TEXT] = PropertyType.RICH_TEXT
    rich_text: NotionEmptyDict


class RollupProperty(_BaseProperty):
    type: Literal[PropertyType.ROLLUP] = PropertyType.ROLLUP
    rollup: Rollup


class SelectProperty(_BaseProperty):
    type: Literal[PropertyType.SELECT] = PropertyType.SELECT
    select: SelectOptions


class StatusProperty(_BaseProperty):
    type: Literal[PropertyType.STATUS] = PropertyType.STATUS
    status: StatusOptions
    groups: Optional[list[GroupOption]] = None


class TitleProperty(_BaseProperty):
    type: Literal[PropertyType.TITLE] = PropertyType.TITLE
    title: NotionEmptyDict


class UrlProperty(_BaseProperty):
    type: Literal[PropertyType.URL] = PropertyType.URL
    url: NotionEmptyDict


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
