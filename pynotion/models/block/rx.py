from typing import Annotated, Optional, Literal, TYPE_CHECKING, Union

from pydantic import BeforeValidator, Tag, Discriminator, ConfigDict

from pynotion.models.block.types import BlockType
from pynotion.models.file import FileType
from pynotion.models.object import NotionObjectId, NotionObjectType
from .common import model_synced_discriminator
from .._internal import FrozenNotionModel, validate_url
from .._internal.utils import discriminate_field

if TYPE_CHECKING:
    from pynotion.models.file import (
        NotionFile,
        HostedFileObject,
        ExternalFileObject,
    )
    from pynotion.models.types import (
        NotionUrlWrapper,
        NotionDatetime,
        NotionEquation,
        NotionEmptyDict,
    )
    from pynotion.models.parent import NotionParent
    from pynotion.models.user import UserRef
    from pynotion.models.block.types import ProgrammingLanguage
    from pynotion.models.block.common import TableOfContents

__all__ = [
    "ChildDatabase",
    "ChildPage",
    "RxBlock",
    "RxBookmark",
    "RxBookmarkBlock",
    "RxBreadcrumbBlock",
    "RxBulletListItem",
    "RxBulletListItemBlock",
    "RxCallout",
    "RxCalloutBlock",
    "RxCaptionExternalFile",
    "RxCaptionExternalFileWithName",
    "RxCaptionFile",
    "RxCaptionFileWithName",
    "RxCaptionHostedFile",
    "RxCaptionHostedFileWithName",
    "RxTableRow",
    "RxTable",
    "RxChildDatabaseBlock",
    "RxChildPageBlock",
    "RxCode",
    "RxCodeBlock",
    "RxColumnBlock",
    "RxColumnListBlock",
    "RxDividerBlock",
    "RxEmbedBlock",
    "RxEquationBlock",
    "RxFileBlock",
    "RxHeading",
    "RxHeadingOneBlock",
    "RxHeadingThreeBlock",
    "RxHeadingTwoBlock",
    "RxImageBlock",
    "RxNumberedListItem",
    "RxNumberedListItemBlock",
    "RxOriginalSynced",
    "RxParagraph",
    "RxParagraphBlock",
    "RxPdfBlock",
    "RxQuote",
    "RxQuoteBlock",
    "RxSynced",
    "RxSyncedBlock",
    "RxTableBlock",
    "RxTableContentBlock",
    "RxTableRowBlock",
    "RxToDo",
    "RxToDoBlock",
    "RxToggle",
    "RxToggleBlock",
    "RxUnsupportedBlock",
    "RxVideoBlock",
    "RX_CAPTION_FILE_CLASS_MAP",
    "RX_CAPTION_FILE_WITH_NAME_CLASS_MAP",
    "RX_BLOCK_CLASS_MAP",
]

RxRichTexts = list["RxRichText"]
RxCaption = Optional[list["RxRichText"]]


class ChildDatabase(FrozenNotionModel):
    """Represents a child database.

    Attributes:
        title: The plain text title of the database.
    """

    title: str


class ChildPage(FrozenNotionModel):
    """Represents a child page.

    Attributes:
        title: The plain text title of the page.
    """

    title: str


class _RxTextBaseBlockObject(FrozenNotionModel):
    """Represents a text base block object.

    Attributes:
        rich_text: The rich text displayed.
        children: The nested child blocks.
        color: The color of the block.
    """

    rich_text: "RxRichTexts"
    children: Optional[list["RxBlock"]] = None
    color: "Color | BackgroundColor"


class RxBookmark(FrozenNotionModel):
    """Represents a bookmark.

    Attributes:
        caption: The caption of the bookmark.
        url: The link for the bookmark.
    """

    caption: "RxCaption" = None
    url: Annotated[str, BeforeValidator(validate_url)]


class RxBulletListItem(_RxTextBaseBlockObject):
    """Bulleted list item block objects"""

    pass


class RxCallout(FrozenNotionModel):
    """Represents a callout.

    Attributes:
        rich_text: the rich texts in the block.
        icon: An emoji or file object that represents the callout's icon.
            If the callout does not have an icon.
        color: the color of the block.
    """

    rich_text: "RxRichTexts"
    icon: Optional["NotionEmoji | NotionFile"]
    color: "Color | BackgroundColor"


class RxCode(FrozenNotionModel):
    """Represents a code block.

    Attributes:
        caption: The rich text in the caption of the code block.
        rich_text: 	The rich text in the code block.
        language: The language of the code contained in the code block.
    """

    caption: "RxCaption" = None
    rich_text: "RxRichTexts"
    language: "ProgrammingLanguage"


class RxCaptionHostedFile(FrozenNotionModel):
    """Represents a hosted file.

    Attributes:
        type: The type of the file.
        file: The hosted file object.
        caption: The caption of the file.
    """

    type: Literal[FileType.FILE] = FileType.FILE
    file: "HostedFileObject"
    caption: "RxCaption" = None


class RxCaptionExternalFile(FrozenNotionModel):
    """Represents an external file.

    Attributes:
        type: The type of the file.
        external: The URL of the externally hosted file.
        caption: The caption of the file.
    """

    type: Literal[FileType.EXTERNAL] = FileType.EXTERNAL
    external: "ExternalFileObject"
    caption: "RxCaption" = None


RX_CAPTION_FILE_CLASS_MAP = {
    FileType.FILE: "RxCaptionHostedFile",
    FileType.EXTERNAL: "RxCaptionExternalFile",
}

RxCaptionFile = Annotated[
    Union[tuple(RX_CAPTION_FILE_CLASS_MAP.values())],
    BeforeValidator(lambda v: discriminate_field(v, "type", RX_CAPTION_FILE_CLASS_MAP)),
]


class RxCaptionHostedFileWithName(RxCaptionHostedFile):
    """Represents a hosted file with a name.

    Attributes:
        type: The type of the file.
        file: The hosted file object.
        caption: The caption of the file.
        name: The name of the file.
    """

    name: str


class RxCaptionExternalFileWithName(RxCaptionExternalFile):
    """Represents an external file with a name.

    Attributes:
        type: The type of the file.
        external: The URL of the externally hosted file.
        caption: The caption of the file.
        name: The name of the file.
    """

    name: str


RX_CAPTION_FILE_WITH_NAME_CLASS_MAP = {
    FileType.FILE: "RxCaptionHostedFileWithName",
    FileType.EXTERNAL: "RxCaptionExternalFileWithName",
}

RxCaptionFileWithName = Annotated[
    Union[tuple(RX_CAPTION_FILE_WITH_NAME_CLASS_MAP.values())],
    BeforeValidator(
        lambda v: discriminate_field(v, "type", RX_CAPTION_FILE_WITH_NAME_CLASS_MAP)
    ),
]


class RxHeading(FrozenNotionModel):
    """Represents a heading.

    Attributes:
        rich_text: The rich texts in the heading.
        color: The color of the heading.
        is_toggleable: Whether the heading is toggleable.
    """

    rich_text: "RxRichTexts"
    color: "Color | BackgroundColor"
    is_toggleable: bool


class RxNumberedListItem(_RxTextBaseBlockObject):
    """Represents a numbered list item."""

    pass


class RxParagraph(_RxTextBaseBlockObject):
    """Represents a paragraph."""

    pass


class RxQuote(_RxTextBaseBlockObject):
    """Represents a quote."""

    pass


class RxOriginalSynced(FrozenNotionModel):
    """Represents an original synced block.

    Attributes:
        synced_from: Always None
        children: The nested child blocks.
    """

    synced_from: None = None
    children: Optional[list["RxBlock"]] = None


RxSynced = Annotated[
    Annotated["RxOriginalSynced", Tag("original")]
    | Annotated["DuplicateSynced", Tag("duplicated")],
    Discriminator(model_synced_discriminator),
]


class RxTableRow(FrozenNotionModel):
    """Represents the cells of a table.

    Attributes:
        cells: the rich texts in the cell.
    """

    cells: Optional[list["RxRichTexts"]] = None


class RxTable(FrozenNotionModel):
    """Represents a table.

    Attributes:
        table_width: The number of columns in the table.
        has_column_header: Whether the table has a column header.
        has_row_header: Whether the table has a row header.
    """

    table_width: int
    has_column_header: bool
    has_row_header: bool
    children: Optional[list["RxTableRowBlock"]] = None


class RxToDo(_RxTextBaseBlockObject):
    """Represents a to-do.

    Attributes:
        checked: Whether the to-do is checked.
    """

    checked: bool


class RxToggle(_RxTextBaseBlockObject):
    """Represents a toggle."""

    pass


class _RxBaseBlock(FrozenNotionModel):
    """Represents a base block.

    Attributes:
        object: The type of the block.
        id: The ID of the block.
        parent: The parent of the block.
        created_time: The creation time of the block.
        last_edited_time: The last edited time of the block.
        created_by: The creator of the block.
        last_edited_by: The last editor of the block.
        archived: Whether the block is archived.
        in_trash: Whether the block is in the trash.
        has_children: Whether the block has children.
    """

    object: "Literal[NotionObjectType.BLOCK]" = "block"
    id: NotionObjectId
    parent: Optional["NotionParent"] = None
    created_time: Optional["NotionDatetime"] = None
    last_edited_time: Optional["NotionDatetime"] = None
    created_by: Optional["UserRef"] = None
    last_edited_by: Optional["UserRef"] = None
    archived: Optional[bool] = None
    in_trash: Optional[bool] = None
    has_children: Optional[bool] = None


class RxBookmarkBlock(_RxBaseBlock):
    """Represents a bookmark.

    Attributes:
        type: The type of the block.
        bookmark: The bookmark object.
    """

    type: Literal[BlockType.BOOKMARK] = BlockType.BOOKMARK
    bookmark: "RxBookmark"


class RxBreadcrumbBlock(_RxBaseBlock):
    """Represents a breadcrumb.

    Attributes:
        type: The type of the block.
        breadcrumb: The breadcrumb object
    """

    type: Literal[BlockType.BREADCRUMB] = BlockType.BREADCRUMB
    breadcrumb: "NotionEmptyDict"


class RxBulletListItemBlock(_RxBaseBlock):
    """Represents a bullet list item.

    Attributes:
        type: the type of the block.
        bulleted_list_item: the bullet list item
    """

    type: Literal[BlockType.BULLETED_LIST_ITEM] = BlockType.BULLETED_LIST_ITEM
    bulleted_list_item: "RxBulletListItem"


class RxCalloutBlock(_RxBaseBlock):
    """Represents a callout.

    Attributes:
        type: the type of the block.
        callout: the callout
    """

    type: Literal[BlockType.CALLOUT] = BlockType.CALLOUT
    callout: "RxCallout"


class RxChildDatabaseBlock(_RxBaseBlock):
    """Represents a child database

    Attributes:
        type: the type of the block.
        child_database: the child block
    """

    type: Literal[BlockType.CHILD_DATABASE] = BlockType.CHILD_DATABASE
    child_database: "ChildDatabase"


class RxChildPageBlock(_RxBaseBlock):
    """Represents a child page

    Attributes:
        type: the type of the block.
        child_page: the child page.
    """

    type: Literal[BlockType.CHILD_PAGE] = BlockType.CHILD_PAGE
    child_page: "ChildPage"


class RxCodeBlock(_RxBaseBlock):
    """Represents a code block.

    Attributes:
        type: the type of the block.
        code: the code.
    """

    type: Literal[BlockType.CODE] = BlockType.CODE
    code: "RxCode"


class RxColumnListBlock(_RxBaseBlock):
    """Represents a column list block.

    Attributes:
        type: the type of the block.
        column_list: the column list.
    """

    type: Literal[BlockType.COLUMN_LIST] = BlockType.COLUMN_LIST
    column_list: "NotionEmptyDict"


class RxColumnBlock(_RxBaseBlock):
    """Represents a column block.

    Attributes:
        type: the type of the block.
        column: the column.
    """

    type: Literal[BlockType.COLUMN] = BlockType.COLUMN
    column: "NotionEmptyDict"


class RxDividerBlock(_RxBaseBlock):
    """Represents a divider block.

    Attributes:
        type: the type of the block.
        divider: the divider
    """

    type: Literal[BlockType.DIVIDER] = BlockType.DIVIDER
    divider: "NotionEmptyDict"


class RxEmbedBlock(_RxBaseBlock):
    """Represents an embed block.

    Attributes:
        type: the type of the block.
        embed: the embed
    """

    type: Literal[BlockType.EMBED] = BlockType.EMBED
    embed: "NotionUrlWrapper"


class RxEquationBlock(_RxBaseBlock):
    """Represents an equation block.

    Attributes:
        type: the type of the block.
        equation: the equation
    """

    type: Literal[BlockType.EQUATION] = BlockType.EQUATION
    equation: "NotionEquation"


class RxFileBlock(_RxBaseBlock):
    """Represents a file block.

    Attributes:
        type: the type of the block.
        file: the file
    """

    type: Literal[BlockType.FILE] = BlockType.FILE
    file: "RxCaptionFileWithName"


class RxHeadingOneBlock(_RxBaseBlock):
    """Represents a heading 1 block.

    Attributes:
        type: the type of the block.
        heading_1: the heading
    """

    type: Literal[BlockType.HEADING_1] = BlockType.HEADING_1
    heading_1: "RxHeading"


class RxHeadingTwoBlock(_RxBaseBlock):
    """Represents a heading 2 block.

    Attributes:
        type: the type of the block.
        heading_2: the heading
    """

    type: Literal[BlockType.HEADING_2] = BlockType.HEADING_2
    heading_2: "RxHeading"


class RxHeadingThreeBlock(_RxBaseBlock):
    """Represents a heading 3 block.

    Attributes:
        type: the type of the block.
        heading_3: the heading
    """

    type: Literal[BlockType.HEADING_3] = BlockType.HEADING_3
    heading_3: "RxHeading"


class RxImageBlock(_RxBaseBlock):
    """Represents an image block.

    Attributes:
        type: the type of the block.
        image: the image
    """

    type: Literal[BlockType.IMAGE] = BlockType.IMAGE
    image: "NotionFile"


class RxNumberedListItemBlock(_RxBaseBlock):
    """Represents a numbered list item block.

    Attributes:
        type: the type of the block.
        numbered_list_item: the numbered list item
    """

    type: Literal[BlockType.NUMBERED_LIST_ITEM] = BlockType.NUMBERED_LIST_ITEM
    numbered_list_item: "RxNumberedListItem"


class RxParagraphBlock(_RxBaseBlock):
    """Represents a paragraph block.

    Attributes:
        type: the type of the block.
        paragraph: the paragraph
    """

    type: Literal[BlockType.PARAGRAPH] = BlockType.PARAGRAPH
    paragraph: "RxParagraph"


class RxPdfBlock(_RxBaseBlock):
    """Represents a PDF block.

    Attributes:
        type: the type of the block.
        pdf: the PDF
    """

    type: Literal[BlockType.PDF] = BlockType.PDF
    pdf: "RxCaptionFile"


class RxQuoteBlock(_RxBaseBlock):
    """Represents a quote block.

    Attributes:
        type: the type of the block.
        quote: the quote
    """

    type: Literal[BlockType.QUOTE] = BlockType.QUOTE
    quote: "RxQuote"


class RxSyncedBlock(_RxBaseBlock):
    """Represents a synced block.

    Attributes:
        type: the type of the block.
        synced_block: the synced block
    """

    type: Literal[BlockType.SYNCED_BLOCK] = BlockType.SYNCED_BLOCK
    synced_block: "RxSynced"


class RxTableBlock(_RxBaseBlock):
    """Represents a table block.

    Attributes:
        type: the type of the block.
        table: the table
    """

    type: Literal[BlockType.TABLE] = BlockType.TABLE
    table: "RxTable"


class RxTableRowBlock(_RxBaseBlock):
    """Represents a table row block.

    Attributes:
        type: the type of the block.
        table_row: the table row
    """

    type: Literal[BlockType.TABLE_ROW] = BlockType.TABLE_ROW
    table_row: "RxTableRow"


class RxTableContentBlock(_RxBaseBlock):
    """Represents a table of contents block.

    Attributes:
        type: the type of the block.
        table_of_contents: the table of contents
    """

    type: Literal[BlockType.TABLE_OF_CONTENTS] = BlockType.TABLE_OF_CONTENTS
    table_of_contents: "TableOfContents"


class RxToDoBlock(_RxBaseBlock):
    """Represents a to-do block.

    Attributes:
        type: the type of the block.
        to_do: the to-do
    """

    type: Literal[BlockType.TO_DO] = BlockType.TO_DO
    to_do: "RxToDo"


class RxToggleBlock(_RxBaseBlock):
    """Represents a toggle block.

    Attributes:
        type: the type of the block.
        toggle: the toggle
    """

    type: Literal[BlockType.TOGGLE] = BlockType.TOGGLE
    toggle: "RxToggle"


class RxVideoBlock(_RxBaseBlock):
    """Represents a video block.

    Attributes:
        type: the type of the block.
        video: the video
    """

    type: Literal[BlockType.VIDEO] = BlockType.VIDEO
    video: "RxCaptionFile"


class RxUnsupportedBlock(_RxBaseBlock):
    """Represents an unsupported block.

    Attributes:
        type: the type of the block.
        unsupported: the unsupported
    """

    model_config = ConfigDict(
        extra="allow", populate_by_name=True, arbitrary_types_allowed=True, frozen=True
    )

    type: Literal[BlockType.UNSUPPORTED] = BlockType.UNSUPPORTED
    unsupported: dict


RX_BLOCK_CLASS_MAP = {
    BlockType.BOOKMARK: "RxBookmarkBlock",
    BlockType.BREADCRUMB: "RxBreadcrumbBlock",
    BlockType.BULLETED_LIST_ITEM: "RxBulletListItemBlock",
    BlockType.CALLOUT: "RxCalloutBlock",
    BlockType.CHILD_DATABASE: "RxChildDatabaseBlock",
    BlockType.CHILD_PAGE: "RxChildPageBlock",
    BlockType.CODE: "RxCodeBlock",
    BlockType.COLUMN: "RxColumnBlock",
    BlockType.COLUMN_LIST: "RxColumnListBlock",
    BlockType.DIVIDER: "RxDividerBlock",
    BlockType.EMBED: "RxEmbedBlock",
    BlockType.EQUATION: "RxEquationBlock",
    BlockType.FILE: "RxFileBlock",
    BlockType.HEADING_1: "RxHeadingOneBlock",
    BlockType.HEADING_2: "RxHeadingTwoBlock",
    BlockType.HEADING_3: "RxHeadingThreeBlock",
    BlockType.IMAGE: "RxImageBlock",
    BlockType.NUMBERED_LIST_ITEM: "RxNumberedListItemBlock",
    BlockType.PARAGRAPH: "RxParagraphBlock",
    BlockType.PDF: "RxPdfBlock",
    BlockType.QUOTE: "RxQuoteBlock",
    BlockType.SYNCED_BLOCK: "RxSyncedBlock",
    BlockType.TABLE: "RxTableBlock",
    BlockType.TABLE_ROW: "RxTableRowBlock",
    BlockType.TABLE_OF_CONTENTS: "RxTableContentBlock",
    BlockType.TO_DO: "RxToDoBlock",
    BlockType.TOGGLE: "RxToggleBlock",
    BlockType.VIDEO: "RxVideoBlock",
    BlockType.UNSUPPORTED: "RxUnsupportedBlock",
}

RxBlock = Annotated[
    Union[tuple(RX_BLOCK_CLASS_MAP.values())],
    BeforeValidator(lambda v: discriminate_field(v, "type", RX_BLOCK_CLASS_MAP)),
]
