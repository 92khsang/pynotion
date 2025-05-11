from __future__ import annotations as _annotations

from enum import Enum
from typing import Optional, Literal, TypeVar, Any, Annotated, TYPE_CHECKING, Union
from uuid import UUID

from pydantic import Field

from ._internal import BaseNotionModel, FrozenNotionModel

if TYPE_CHECKING:
    from pynotion.models import (
        RxBlock,
        RxComment,
        RxDatabase,
        RxPage,
        RxPropertyItem,
        RxPaginatedPropertyItem,
        NotionDatetime,
        NotionEmptyDict,
        NotionUser,
    )

__all__ = [
    # Pagination
    "PaginatedItem",
    "PaginationType",
    "BlockPagination",
    "CommentPagination",
    "DatabasePagination",
    "PagePagination",
    "PageOrDatabasePagination",
    "PropertyItemPagination",
    "UserPagination",
    "TxPagination",
    # Sort
    "SortDirection",
    "PropertySort",
    "TimestampSort",
    "NotionSort",
    # Filters
    "CheckboxCondition",
    "DateCondition",
    "FilesCondition",
    "MultiSelectCondition",
    "NumberCondition",
    "PersonCondition",
    "RelationCondition",
    "RichTextCondition",
    "SelectCondition",
    "StatusCondition",
    "UniqueIdCondition",
    "FormulaCondition",
    "RollupCondition",
    "FilterCondition",
    "CheckboxFilter",
    "DateFilter",
    "FilesFilter",
    "FormulaFilter",
    "MultiSelectFilter",
    "NumberFilter",
    "PeopleFilter",
    "RelationFilter",
    "RichTextFilter",
    "RollupFilter",
    "SelectFilter",
    "StatusFilter",
    "UniqueIdFilter",
    "CreatedTimeFilter",
    "LastEditedTimeFilter",
    "AndPropertyFilter",
    "OrPropertyFilter",
    "PropertyFilter",
    "ObjectFilter",
]

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
    """Represents a paginated list of items.

    Attributes:
        object: The type of the object. Always "list".
        has_more: Whether there are more items.
        next_cursor: The cursor to use for the next page.
    """

    object: Literal["list"] = "list"
    has_more: bool
    next_cursor: Optional[str]


class BlockPagination(_RxBasePagination):
    """Represents a paginated list of blocks.

    Attributes:
        type: The type of the pagination. Always "block".
        block: The block to paginate.
        results: The list of blocks.
    """

    type: Literal[PaginationType.BLOCK] = PaginationType.BLOCK
    block: Any = None
    results: list["RxBlock"]


class CommentPagination(_RxBasePagination):
    """Represents a paginated list of comments.

    Attributes:
        type: The type of the pagination. Always "comment".
        comment: The comment to paginate.
        results: The list of comments.
    """

    type: Literal[PaginationType.COMMENT] = PaginationType.COMMENT
    comment: Any = None
    results: list["RxComment"]


class DatabasePagination(_RxBasePagination):
    """Represents a paginated list of databases.

    Attributes:
        type: The type of the pagination. Always "database".
        database: The database to paginate.
        results: The list of databases.
    """

    type: Literal[PaginationType.DATABASE] = PaginationType.DATABASE
    database: Any = None
    results: list["RxDatabase"]


class PagePagination(_RxBasePagination):
    """Represents a paginated list of pages.

    Attributes:
        type: The type of the pagination. Always "page".
        page: The page to paginate.
        results: The list of pages.
    """

    type: Literal[PaginationType.PAGE] = PaginationType.PAGE
    page: Any = None
    results: list["RxPage"]


class PageOrDatabasePagination(_RxBasePagination):
    """Represents a paginated list of pages or databases.

    Attributes:
        type: The type of the pagination. Always "page_or_database".
        page_or_database: The page or database to paginate.
        results: The list of pages or databases.
    """

    type: Literal[PaginationType.PAGE_OR_DATABASE] = PaginationType.PAGE_OR_DATABASE
    page_or_database: Any = None
    results: list[
        Annotated[Union["RxPage", "RxDatabase"], Field(discriminator="object")]
    ]


class PropertyItemPagination(_RxBasePagination):
    """Represents a paginated list of property items.

    Attributes:
        type: The type of the pagination. Always "property_item".
        property_item: The property item to paginate.
        results: The list of property items.
    """

    type: Literal[PaginationType.PROPERTY_ITEM] = PaginationType.PROPERTY_ITEM
    property_item: Optional["RxPropertyItem"] = None
    results: list["RxPaginatedPropertyItem"]


class UserPagination(_RxBasePagination):
    """Represents a paginated list of users.

    Attributes:
        type: The type of the pagination. Always "user".
        user: The user to paginate.
        results: The list of users.
    """

    type: Literal[PaginationType.USER] = PaginationType.USER
    user: Any = None
    results: list["NotionUser"]


class TxPagination(BaseNotionModel):
    """Model for pagination in a transaction.

    Attributes:
        page_size: The number of items to return per page.
        start_cursor: The cursor to use for the first page.
    """

    page_size: int = 100
    start_cursor: Optional[str] = None


class SortDirection(str, Enum):
    DESCENDING = "descending"
    ASCENDING = "ascending"


class PropertySort(BaseNotionModel):
    """Model for sorting by a property.

    Attributes:
        property: The property to sort by.
        direction: The direction to sort in.
    """

    property: str
    direction: "SortDirection"


class TimestampSort(BaseNotionModel):
    """Model for sorting by a timestamp.

    Attributes:
        timestamp: The timestamp to sort by.
        direction: The direction to sort in.
    """

    timestamp: Literal["created_time", "last_edited_time"]
    direction: "SortDirection"


NotionSort = Union[PropertySort, TimestampSort]


class CheckboxCondition(BaseNotionModel):
    """Model for a checkbox condition.

    Attributes:
        equals: Whether the checkbox is checked.
        does_not_equal: Whether the checkbox is not checked.
    """

    equals: Optional[bool] = None
    does_not_equal: Optional[bool] = None


class DateCondition(BaseNotionModel):
    """Model for a date condition.

    Attributes:
        before: The date before.
        after: The date after.
        equals: The date equals.
        is_empty: Whether the date is empty.
        is_not_empty: Whether the date is not empty.
        next_month: The next month.
        next_week: The next week.
        next_year: The next year.
        on_or_before: The date on or before.
        on_or_after: The date on or after.
        past_month: The past month.
        past_week: The past week.
        past_year: The past year.
        this_week: The current week.
    """

    before: Optional["NotionDatetime"] = None
    after: Optional["NotionDatetime"] = None
    equals: Optional["NotionDatetime"] = None
    is_empty: Optional[bool] = None
    is_not_empty: Optional[bool] = None
    next_month: Optional["NotionEmptyDict"] = None
    next_week: Optional["NotionEmptyDict"] = None
    next_year: Optional["NotionEmptyDict"] = None
    on_or_before: Optional["NotionDatetime"] = None
    on_or_after: Optional["NotionDatetime"] = None
    past_month: Optional["NotionEmptyDict"] = None
    past_week: Optional["NotionEmptyDict"] = None
    past_year: Optional["NotionEmptyDict"] = None
    this_week: Optional["NotionEmptyDict"] = None


class FilesCondition(BaseNotionModel):
    """Model for a 'files' condition.

    Attributes:
        is_empty: Whether the files are empty.
        is_not_empty: Whether the files are not empty.
    """

    is_empty: Optional[bool] = None
    is_not_empty: Optional[bool] = None


class MultiSelectCondition(BaseNotionModel):
    """Model for a multi-select condition.

    Attributes:
        contains: The value to contain.
        does_not_contain: The value to not contain.
        is_empty: Whether the multi-select is empty.
        is_not_empty: Whether the multi-select is not empty.
    """

    contains: Optional[str] = None
    does_not_contain: Optional[str] = None
    is_empty: Optional[bool] = None
    is_not_empty: Optional[bool] = None


class NumberCondition(BaseNotionModel):
    """Model for a number condition.

    Attributes:
        does_not_equal: The value to not equal.
        equals: The value to equal.
        greater_than: The value to be greater than.
        greater_than_or_equal_to: The value to be greater than or equal to.
        less_than: The value to be less than.
        less_than_or_equal_to: The value to be less than or equal to.
        is_empty: Whether the number is empty.
        is_not_empty: Whether the number is not empty.
    """

    does_not_equal: Optional[float | int] = None
    equals: Optional[float | int] = None
    greater_than: Optional[float | int] = None
    greater_than_or_equal_to: Optional[float | int] = None
    less_than: Optional[float | int] = None
    less_than_or_equal_to: Optional[float | int] = None
    is_empty: Optional[bool] = None
    is_not_empty: Optional[bool] = None


class PersonCondition(BaseNotionModel):
    """Model for a 'person' condition.

    Attributes:
        contains: The person to contain.
        does_not_contain: The person to not contain.
        is_empty: Whether the person is empty.
        is_not_empty: Whether the person is not empty.
    """

    contains: Optional[UUID] = None
    does_not_contain: Optional[UUID] = None
    is_empty: Optional[bool] = None
    is_not_empty: Optional[bool] = None


class RelationCondition(BaseNotionModel):
    """Model for a relation condition.

    Attributes:
        contains: The relation to contain.
        does_not_contain: The relation to not contain.
        is_empty: Whether the relation is empty.
        is_not_empty: Whether the relation is not empty.
    """

    contains: Optional[UUID] = None
    does_not_contain: Optional[UUID] = None
    is_empty: Optional[bool] = None
    is_not_empty: Optional[bool] = None


class RichTextCondition(BaseNotionModel):
    """Model for a rich text condition.

    Attributes:
        contains: The text to contain.
        does_not_contain: The text does not contain.
        equals: The text to equal.
        does_not_equal: The text to not equal.
        is_empty: Whether the rich text is empty.
        is_not_empty: Whether the rich text is not empty.
        starts_with: The text to start with.
        ends_with: The text to end with.
    """

    contains: Optional[str] = None
    does_not_contain: Optional[str] = None
    equals: Optional[str] = None
    does_not_equal: Optional[str] = None
    is_empty: Optional[bool] = None
    is_not_empty: Optional[bool] = None
    starts_with: Optional[str] = None
    ends_with: Optional[str] = None


class SelectCondition(BaseNotionModel):
    """Model for a select condition.

    Attributes:
        equals: The value to equal.
        does_not_equal: The value to not equal.
        is_empty: Whether the select is empty.
        is_not_empty: Whether the select is not empty.
    """

    equals: Optional[str] = None
    does_not_equal: Optional[str] = None
    is_empty: Optional[bool] = None
    is_not_empty: Optional[bool] = None


class StatusCondition(BaseNotionModel):
    """Model for a status condition.

    Attributes:
        equals: The value to equal.
        does_not_equal: The value to not equal.
        is_empty: Whether the status is empty.
        is_not_empty: Whether the status is not empty.
    """

    equals: Optional[str] = None
    does_not_equal: Optional[str] = None
    is_empty: Optional[bool] = None
    is_not_empty: Optional[bool] = None


class UniqueIdCondition(BaseNotionModel):
    """Model for a unique id condition.

    Attributes:
        equals: The value to equal.
        does_not_equal: The value to not equal.
        greater_than: The value to be greater than.
        greater_than_or_equal_to: The value to be greater than or equal to.
        less_than: The value to be less than.
        less_than_or_equal_to: The value to be less than or equal to.
    """

    equals: Optional[str] = None
    does_not_equal: Optional[str] = None
    greater_than: Optional[float | int] = None
    greater_than_or_equal_to: Optional[float | int] = None
    less_than: Optional[float | int] = None
    less_than_or_equal_to: Optional[float | int] = None


class FormulaCondition(BaseNotionModel):
    """Model for a formula condition.

    Attributes:
        checkbox: The checkbox condition.
        date: The date condition.
        number: The number condition.
        string: The string condition.
    """

    checkbox: Optional["CheckboxCondition"] = None
    date: Optional["DateCondition"] = None
    number: Optional["NumberCondition"] = None
    string: Optional["RichTextCondition"] = None


class RollupCondition(BaseNotionModel):
    """Model for a rollup condition.

    Attributes:
        any: Any condition.
        every: The every condition.
        none: The none condition.
        date: The date condition.
        number: The number condition.
    """

    any: Optional[list["FilterCondition"]] = None
    every: Optional[list["FilterCondition"]] = None
    none: Optional[list["FilterCondition"]] = None
    date: Optional["DateCondition"] = None
    number: Optional["NumberCondition"] = None


FilterCondition = Union[
    "CheckboxCondition",
    "DateCondition",
    "FilesCondition",
    "MultiSelectCondition",
    "NumberCondition",
    "PersonCondition",
    "RelationCondition",
    "RichTextCondition",
    "SelectCondition",
    "StatusCondition",
    "UniqueIdCondition",
    "FormulaCondition",
    "RollupCondition",
]


class _BasePropertyFilter(BaseNotionModel):
    """Model for a property filter.

    Attributes:
        property: The property to filter.
    """

    property: str


class _BaseTimestampFilter(BaseNotionModel):
    """Model for a timestamp filter.

    Attributes:
        timestamp: The timestamp to filter by.
    """

    timestamp: Literal["created_time", "last_edited_time"]


class CheckboxFilter(_BasePropertyFilter):
    """Model for a checkbox filter.

    Attributes:
        checkbox: The checkbox condition.
    """

    checkbox: "CheckboxCondition"


class DateFilter(_BasePropertyFilter):
    """Model for a date filter.

    Attributes:
        date: The date condition.
    """

    date: "DateCondition"


class FilesFilter(_BasePropertyFilter):
    """Model for 'files' filter.

    Attributes:
        files: The 'files' condition
    """

    files: "FilesCondition"


class FormulaFilter(_BasePropertyFilter):
    """Model for a formula filter.

    Attributes:
        formula: The formula condition
    """

    formula: "FormulaCondition"


class MultiSelectFilter(_BasePropertyFilter):
    """Model for a multi select filter.

    Attributes:
        multi_select: The multi select condition
    """

    multi_select: "MultiSelectCondition"


class NumberFilter(_BasePropertyFilter):
    """Model for a number filter.

    Attributes:
        number: The number condition
    """

    number: "NumberCondition"


class PeopleFilter(_BasePropertyFilter):
    """Model for a people filter.

    Attributes:
        people: The people condition
    """

    people: "PersonCondition"


class RelationFilter(_BasePropertyFilter):
    """Model for a relation filter.

    Attributes:
        relation: The relation condition
    """

    relation: "RelationCondition"


class RichTextFilter(_BasePropertyFilter):
    """Model for a rich text filter.

    Attributes:
        rich_text: The rich text condition
    """

    rich_text: "RichTextCondition"


class RollupFilter(_BasePropertyFilter):
    """Model for a rollup filter.

    Attributes:
        rollup: The rollup condition
    """

    rollup: "RollupCondition"


class SelectFilter(_BasePropertyFilter):
    """Model for a select filter.

    Attributes:
        select: The select condition
    """

    select: "SelectCondition"


class StatusFilter(_BasePropertyFilter):
    """Model for a status filter.

    Attributes:
        status: The status condition
    """

    status: "StatusCondition"


class UniqueIdFilter(_BasePropertyFilter):
    """Model for a unique id filter.

    Attributes:
        unique_id: The unique id condition
    """

    unique_id: "UniqueIdCondition"


class CreatedTimeFilter(_BaseTimestampFilter):
    """Model for a created time filter.

    Attributes:
        created_time: The created time condition
    """

    created_time: "DateCondition"


class LastEditedTimeFilter(_BaseTimestampFilter):
    """Model for a last edited time filter.

    Attributes:
        last_edited_time: The last edited time condition
    """

    last_edited_time: "DateCondition"


class AndPropertyFilter(BaseNotionModel):
    """Model for an and property filter.

    Attributes:
        filters: The filters
    """

    filters: list["PropertyFilter"]


class OrPropertyFilter(BaseNotionModel):
    """Model for an or property filter.

    Attributes:
        filters: The filters
    """

    filters: list["PropertyFilter"]


PropertyFilter = Union[
    "CheckboxFilter",
    "DateFilter",
    "FilesFilter",
    "FormulaFilter",
    "MultiSelectFilter",
    "NumberFilter",
    "PeopleFilter",
    "RelationFilter",
    "RichTextFilter",
    "RollupFilter",
    "SelectFilter",
    "StatusFilter",
    "UniqueIdFilter",
    "CreatedTimeFilter",
    "LastEditedTimeFilter",
    "AndPropertyFilter",
    "OrPropertyFilter",
]


class ObjectFilter(BaseNotionModel):
    """Model for a search query.

    Attributes:
        property: The property to filter.
    """

    property: Literal["object"] = "object"
    value: Literal["database", "page"]
