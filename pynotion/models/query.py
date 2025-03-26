from __future__ import annotations as _annotations

from enum import Enum
from typing import Optional, Literal, TypeVar, Any, Annotated

from pydantic import Field

from ._internal import BaseNotionModel, FrozenNotionModel
from .block import RxBlock
from .comment import RxComment
from .database import RxDatabase
from .object import NotionObjectId
from .page import RxPage
from .properties import RxPropertyItem, RxPaginatedPropertyItem
from .types import NotionDatetime, NotionEmptyDict
from .user import User

PaginatedItem = TypeVar("PaginatedItem")


class PaginationType(str, Enum):
    BLOCK = "block"
    COMMENT = "comment"
    DATABASE = "database"
    PAGE = "page"
    PAGE_OR_DATABASE = "page_or_database"
    PROPERTY_ITEM = "property_item"
    USER = "user"


class _RxBasePagination(FrozenNotionModel):
    object: Literal["list"] = "list"
    has_more: bool
    next_cursor: Optional[str]


class BlockPagination(_RxBasePagination):
    type: Literal[PaginationType.BLOCK] = PaginationType.BLOCK
    block: Any = None
    results: list[RxBlock]


class CommentPagination(_RxBasePagination):
    type: Literal[PaginationType.COMMENT] = PaginationType.COMMENT
    comment: Any = None
    results: list[RxComment]


class DatabasePagination(_RxBasePagination):
    type: Literal[PaginationType.DATABASE] = PaginationType.DATABASE
    database: Any = None
    results: list[RxDatabase]


class PagePagination(_RxBasePagination):
    type: Literal[PaginationType.PAGE] = PaginationType.PAGE
    page: Any = None
    results: list[RxPage]


class PageOrDatabasePagination(_RxBasePagination):
    type: Literal[PaginationType.PAGE_OR_DATABASE] = PaginationType.PAGE_OR_DATABASE
    page_or_database: Any = None
    results: list[RxPage | RxDatabase]


class PropertyItemPagination(_RxBasePagination):
    type: Literal[PaginationType.PROPERTY_ITEM] = PaginationType.PROPERTY_ITEM
    property_item: Optional[RxPropertyItem] = None
    results: list[RxPaginatedPropertyItem]


class UserPagination(_RxBasePagination):
    type: Literal[PaginationType.USER] = PaginationType.USER
    user: Any = None
    results: list[User]


RxPagination = Annotated[
    BlockPagination
    | CommentPagination
    | DatabasePagination
    | PagePagination
    | PageOrDatabasePagination
    | PropertyItemPagination
    | UserPagination,
    Field(discriminator="type"),
]


class TxPagination(BaseNotionModel):
    page_size: int = 100
    start_cursor: Optional[str] = None


class SortDirection(str, Enum):
    DESCENDING = "descending"
    ASCENDING = "ascending"


class PropertySort(BaseNotionModel):
    property: str
    direction: SortDirection


class TimestampSort(BaseNotionModel):
    timestamp: Literal["created_time", "last_edited_time"]
    direction: SortDirection


NotionSort = PropertySort | TimestampSort


class CheckboxCondition(BaseNotionModel):
    equals: Optional[bool]
    does_not_equal: Optional[bool]


class DateCondition(BaseNotionModel):
    before: Optional[NotionDatetime]
    after: Optional[NotionDatetime]
    equals: Optional[NotionDatetime]
    is_empty: Optional[bool]
    is_not_empty: Optional[bool]
    next_month: Optional[NotionEmptyDict]
    next_week: Optional[NotionEmptyDict]
    next_year: Optional[NotionEmptyDict]
    on_or_before: Optional[NotionDatetime]
    on_or_after: Optional[NotionDatetime]
    past_month: Optional[NotionEmptyDict]
    past_week: Optional[NotionEmptyDict]
    past_year: Optional[NotionEmptyDict]
    this_week: Optional[NotionEmptyDict]


class FilesCondition(BaseNotionModel):
    is_empty: Optional[bool]
    is_not_empty: Optional[bool]


class MultiSelectCondition(BaseNotionModel):
    contains: Optional[str]
    does_not_contain: Optional[str]
    is_empty: Optional[bool]
    is_not_empty: Optional[bool]


class NumberCondition(BaseNotionModel):
    does_not_equal: Optional[float | int]
    equals: Optional[float | int]
    greater_than: Optional[float | int]
    greater_than_or_equal_to: Optional[float | int]
    less_than: Optional[float | int]
    less_than_or_equal_to: Optional[float | int]
    is_empty: Optional[bool]
    is_not_empty: Optional[bool]


class PersonCondition(BaseNotionModel):
    contains: Optional[NotionObjectId]
    does_not_contain: Optional[NotionObjectId]
    is_empty: Optional[bool]
    is_not_empty: Optional[bool]


class RelationCondition(BaseNotionModel):
    contains: Optional[NotionObjectId]
    does_not_contain: Optional[NotionObjectId]
    is_empty: Optional[bool]
    is_not_empty: Optional[bool]


class RichTextCondition(BaseNotionModel):
    contains: Optional[str]
    does_not_contain: Optional[str]
    equals: Optional[str]
    does_not_equal: Optional[str]
    is_empty: Optional[bool]
    is_not_empty: Optional[bool]
    starts_with: Optional[str]
    ends_with: Optional[str]


class SelectCondition(BaseNotionModel):
    equals: Optional[str]
    does_not_equal: Optional[str]
    is_empty: Optional[bool]
    is_not_empty: Optional[bool]


class StatusCondition(BaseNotionModel):
    equals: Optional[str]
    does_not_equal: Optional[str]
    is_empty: Optional[bool]
    is_not_empty: Optional[bool]


class UniqueIdCondition(BaseNotionModel):
    equals: Optional[str]
    does_not_equal: Optional[str]
    greater_than: Optional[float | int]
    greater_than_or_equal_to: Optional[float | int]
    less_than: Optional[float | int]
    less_than_or_equal_to: Optional[float | int]


class FormulaCondition(BaseNotionModel):
    checkbox: Optional[CheckboxCondition]
    date: Optional[DateCondition]
    number: Optional[NumberCondition]
    string: Optional[RichTextCondition]


class RollupCondition(BaseNotionModel):
    any: Optional[list[FilterCondition]]
    every: Optional[list[FilterCondition]]
    none: Optional[list[FilterCondition]]
    date: Optional[DateCondition]
    number: Optional[NumberCondition]


FilterCondition = (
    CheckboxCondition
    | DateCondition
    | FilesCondition
    | MultiSelectCondition
    | NumberCondition
    | PersonCondition
    | RelationCondition
    | RichTextCondition
    | SelectCondition
    | StatusCondition
    | UniqueIdCondition
    | FormulaCondition
    | RollupCondition
)


class _BasePropertyFilter(BaseNotionModel):
    property: str


class _BaseTimestampFilter(BaseNotionModel):
    timestamp: Literal["created_time", "last_edited_time"]


class CheckboxFilter(_BasePropertyFilter):
    checkbox: CheckboxCondition


class DateFilter(_BasePropertyFilter):
    date: DateCondition


class FilesFilter(_BasePropertyFilter):
    files: FilesCondition


class FormulaFilter(_BasePropertyFilter):
    formula: FormulaCondition


class MultiSelectFilter(_BasePropertyFilter):
    multi_select: MultiSelectCondition


class NumberFilter(_BasePropertyFilter):
    number: NumberCondition


class PeopleFilter(_BasePropertyFilter):
    people: PersonCondition


class RelationFilter(_BasePropertyFilter):
    relation: RelationCondition


class RichTextFilter(_BasePropertyFilter):
    rich_text: RichTextCondition


class RollupFilter(_BasePropertyFilter):
    rollup: RollupCondition


class SelectFilter(_BasePropertyFilter):
    select: SelectCondition


class StatusFilter(_BasePropertyFilter):
    status: StatusCondition


class UniqueIdFilter(_BasePropertyFilter):
    unique_id: UniqueIdCondition


class CreatedTimeFilter(_BaseTimestampFilter):
    created_time: DateCondition


class LastEditedTimeFilter(_BaseTimestampFilter):
    last_edited_time: DateCondition


class AndPropertyFilter(BaseNotionModel):
    filters: list[PropertyFilter]


class OrPropertyFilter(BaseNotionModel):
    filters: list[PropertyFilter]


PropertyFilter = (
    CheckboxFilter
    | DateFilter
    | FilesFilter
    | FormulaFilter
    | MultiSelectFilter
    | NumberFilter
    | PeopleFilter
    | RelationFilter
    | RichTextFilter
    | RollupFilter
    | SelectFilter
    | StatusFilter
    | UniqueIdFilter
    | CreatedTimeFilter
    | LastEditedTimeFilter
    | AndPropertyFilter
    | OrPropertyFilter
)


class ObjectFilter(BaseNotionModel):
    property: Literal["object"] = "object"
    value: Literal["database", "page"]
