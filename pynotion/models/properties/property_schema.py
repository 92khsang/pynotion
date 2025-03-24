from __future__ import annotations as _annotations

from typing import Literal, Annotated, Optional

from pydantic import (
    Field,
    Discriminator,
    Tag,
)

from .types import NumberFormat, RollupFunction, PropertyType
from .._internal import (
    FrozenNotionModel,
    BaseNotionModel,
)
from ..object import NotionObjectId
from ..types import NotionEquation, Color, NotionEmptyDict


class NumberSchema(BaseNotionModel):
    format: NumberFormat


class DualRelationSchema(FrozenNotionModel):
    database_id: NotionObjectId
    dual_property: NotionEmptyDict


class SingleRelationSchema(FrozenNotionModel):
    database_id: NotionObjectId
    single_property: NotionEmptyDict


def model_relation_schema_discriminator(values):
    from .._internal.utils import get_value_for_discriminator

    dual_property = get_value_for_discriminator(values, "dual_property")
    if dual_property is not None:
        return "dual"
    else:
        return "single"


RelationSchema = Annotated[
    Annotated[SingleRelationSchema, Tag("single")]
    | Annotated[DualRelationSchema, Tag("dual")],
    Discriminator(model_relation_schema_discriminator),
]


class RxBaseOptionSchema(FrozenNotionModel):
    id: str
    name: str
    color: Color


class RxSelectOptionsSchema(FrozenNotionModel):
    options: list[RxBaseOptionSchema]


class RxRollupSchema(FrozenNotionModel):
    relation_property_id: str
    rollup_property_id: str
    relation_property_name: str
    rollup_property_name: str
    function: RollupFunction


class _RxBasePropertySchema(FrozenNotionModel):
    id: str
    name: str


class RxTitlePropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.TITLE] = PropertyType.TITLE
    title: NotionEmptyDict


class RxRichTextPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.RICH_TEXT] = PropertyType.RICH_TEXT
    rich_text: NotionEmptyDict


class RxNumberPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.NUMBER] = PropertyType.NUMBER
    number: NumberSchema


class RxSelectPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.SELECT] = PropertyType.SELECT
    select: RxSelectOptionsSchema


class RxMultiSelectPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.MULTI_SELECT] = PropertyType.MULTI_SELECT
    multi_select: RxSelectOptionsSchema


class RxDatePropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.DATE] = PropertyType.DATE
    date: NotionEmptyDict


class RxPeoplePropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.PEOPLE] = PropertyType.PEOPLE
    people: NotionEmptyDict


class RxFilesPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.FILES] = PropertyType.FILES
    files: NotionEmptyDict


class RxCheckboxPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.CHECKBOX] = PropertyType.CHECKBOX
    checkbox: NotionEmptyDict


class RxUrlPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.URL] = PropertyType.URL
    url: NotionEmptyDict


class RxEmailPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.EMAIL] = PropertyType.EMAIL
    email: NotionEmptyDict


class RxPhoneNumberPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.PHONE_NUMBER] = PropertyType.PHONE_NUMBER
    phone_number: NotionEmptyDict


class RxFormulaPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.FORMULA] = PropertyType.FORMULA
    formula: NotionEquation


class RxRelationPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.RELATION] = PropertyType.RELATION
    relation: RelationSchema


class RxRollupPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.ROLLUP] = PropertyType.ROLLUP
    rollup: RxRollupSchema


class RxCreatedTimePropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.CREATED_TIME] = PropertyType.CREATED_TIME
    created_time: NotionEmptyDict


class RxCreatedByPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.CREATED_BY] = PropertyType.CREATED_BY
    created_by: NotionEmptyDict


class RxLastEditedTimePropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.LAST_EDITED_TIME] = PropertyType.LAST_EDITED_TIME
    last_edited_time: NotionEmptyDict


class RxLastEditedByPropertySchema(_RxBasePropertySchema):
    type: Literal[PropertyType.LAST_EDITED_BY] = PropertyType.LAST_EDITED_BY
    last_edited_by: NotionEmptyDict


RxPropertySchema = Annotated[
    RxTitlePropertySchema
    | RxRichTextPropertySchema
    | RxNumberPropertySchema
    | RxSelectPropertySchema
    | RxMultiSelectPropertySchema
    | RxDatePropertySchema
    | RxPeoplePropertySchema
    | RxFilesPropertySchema
    | RxCheckboxPropertySchema
    | RxUrlPropertySchema
    | RxEmailPropertySchema
    | RxPhoneNumberPropertySchema
    | RxFormulaPropertySchema
    | RxRelationPropertySchema
    | RxRollupPropertySchema
    | RxCreatedTimePropertySchema
    | RxCreatedByPropertySchema
    | RxLastEditedTimePropertySchema
    | RxLastEditedByPropertySchema,
    Field(discriminator="type"),
]


class TxBaseOptionSchema(BaseNotionModel):
    name: str
    color: Optional[Color] = None


class TxSelectOptionsSchema(BaseNotionModel):
    options: list[TxBaseOptionSchema] = Field(default_factory=list)


class TxRollupSchema(BaseNotionModel):
    relation_property_name: str
    rollup_property_name: str
    function: RollupFunction


class TxTitlePropertySchema(BaseNotionModel):
    title: NotionEmptyDict


class TxRichTextPropertySchema(BaseNotionModel):
    rich_text: NotionEmptyDict


class TxNumberPropertySchema(BaseNotionModel):
    number: NumberSchema


class TxSelectPropertySchema(BaseNotionModel):
    select: TxSelectOptionsSchema


class TxMultiSelectPropertySchema(BaseNotionModel):
    multi_select: TxSelectOptionsSchema


class TxDatePropertySchema(BaseNotionModel):
    date: NotionEmptyDict


class TxPeoplePropertySchema(BaseNotionModel):
    people: NotionEmptyDict


class TxFilesPropertySchema(BaseNotionModel):
    files: NotionEmptyDict


class TxCheckboxPropertySchema(BaseNotionModel):
    checkbox: NotionEmptyDict


class TxUrlPropertySchema(BaseNotionModel):
    url: NotionEmptyDict


class TxEmailPropertySchema(BaseNotionModel):
    email: NotionEmptyDict


class TxPhoneNumberPropertySchema(BaseNotionModel):
    phone_number: NotionEmptyDict


class TxFormulaPropertySchema(BaseNotionModel):
    formula: NotionEquation


class TxRelationPropertySchema(BaseNotionModel):
    relation: RelationSchema


class TxRollupPropertySchema(BaseNotionModel):
    rollup: TxRollupSchema


class TxCreatedTimePropertySchema(BaseNotionModel):
    created_time: NotionEmptyDict


class TxCreatedByPropertySchema(BaseNotionModel):
    created_by: NotionEmptyDict


class TxLastEditedTimePropertySchema(BaseNotionModel):
    last_edited_time: NotionEmptyDict


class TxLastEditedByPropertySchema(BaseNotionModel):
    last_edited_by: NotionEmptyDict


TxPropertySchema = (
    TxTitlePropertySchema
    | TxRichTextPropertySchema
    | TxNumberPropertySchema
    | TxSelectPropertySchema
    | TxMultiSelectPropertySchema
    | TxDatePropertySchema
    | TxPeoplePropertySchema
    | TxFilesPropertySchema
    | TxCheckboxPropertySchema
    | TxUrlPropertySchema
    | TxEmailPropertySchema
    | TxPhoneNumberPropertySchema
    | TxFormulaPropertySchema
    | TxRelationPropertySchema
    | TxRollupPropertySchema
    | TxCreatedTimePropertySchema
    | TxCreatedByPropertySchema
    | TxLastEditedTimePropertySchema
    | TxLastEditedByPropertySchema
)
