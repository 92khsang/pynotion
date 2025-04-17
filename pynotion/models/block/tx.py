from typing import Annotated, Optional, Literal, TYPE_CHECKING, Union

from pydantic import (
    BeforeValidator,
    Discriminator,
    Field,
    Tag,
    model_serializer,
    model_validator,
)

from pynotion.models.block.common import model_synced_discriminator
from pynotion.models.block.types import ProgrammingLanguage, BlockType
from pynotion.models.file import FileType
from pynotion.models.object import NotionObjectType
from .._internal import validate_url, validate_enum, BaseNotionModel
from .._internal.utils import discriminate_field

if TYPE_CHECKING:
    from pynotion.models import (
        BackgroundColor,
        Color,
        ExternalFileObject,
        HostedFileObject,
        NotionEmptyDict,
        NotionEquation,
        NotionEmoji,
        NotionFile,
        NotionUrlWrapper,
        TableOfContents,
        TxRichText,
    )


TxColor = Optional[
    Annotated[
        Union["str", "Color", "BackgroundColor"],
        BeforeValidator(lambda v: validate_enum(v, (Color, BackgroundColor))),
    ]
]

__all__ = [
    "TxBlock",
    "TxBookmark",
    "TxBookmarkBlock",
    "TxBreadcrumbBlock",
    "TxBulletListItem",
    "TxBulletListItemBlock",
    "TxCallout",
    "TxCalloutBlock",
    "TxCaptionExternalFile",
    "TxCaptionExternalFileWithName",
    "TxCaptionFile",
    "TxCaptionFileWithName",
    "TxCaptionHostedFile",
    "TxCaptionHostedFileWithName",
    "TxTableRow",
    "TxTable",
    "TxCode",
    "TxCodeBlock",
    "TxColumnChildren",
    "TxColumnBlock",
    "TxColumnBlocks",
    "TxColumnListBlock",
    "TxDividerBlock",
    "TxEmbedBlock",
    "TxEquationBlock",
    "TxFileBlock",
    "TxHeading",
    "TxHeadingOneBlock",
    "TxHeadingThreeBlock",
    "TxHeadingTwoBlock",
    "TxImageBlock",
    "TxNumberedListItem",
    "TxNumberedListItemBlock",
    "TxOriginalSynced",
    "TxParagraph",
    "TxParagraphBlock",
    "TxPdfBlock",
    "TxQuote",
    "TxQuoteBlock",
    "TxSynced",
    "TxSyncedBlock",
    "TxTableBlock",
    "TxTableContentBlock",
    "TxTableRowBlock",
    "TxToDo",
    "TxToDoBlock",
    "TxToggle",
    "TxToggleBlock",
    "TxVideoBlock",
    "TX_CAPTION_FILE_CLASS_MAP",
    "TX_CAPTION_FILE_WITH_NAME_CLASS_MAP",
    "TX_BLOCK_CLASS_MAP",
]


class _TxTextBaseBlockObject(BaseNotionModel):
    """Represents a text-based block value.

    Attributes:
        rich_text: The rich text displayed.
        children: The nested child blocks.
        color: The color of the block.
    """

    rich_text: list["TxRichText"] = Field(default_factory=list)
    children: Optional[list["TxBlock"]] = None
    color: "TxColor" = None


class TxBookmark(BaseNotionModel):
    """Represents a bookmark.

    Attributes:
        caption: The caption of the bookmark.
        url: The link for the bookmark.
    """

    caption: Optional[list["TxRichText"]] = None
    url: Annotated[str, BeforeValidator(validate_url)]


class TxBulletListItem(_TxTextBaseBlockObject):
    """Bulleted list item block objects"""

    pass


class TxCallout(BaseNotionModel):
    """Represents a callout.

    Attributes:
        rich_text: the rich texts in the block.
        icon: An emoji or file object that represents the callout's icon.
            If the callout does not have an icon.
        color: the color of the block.
    """

    rich_text: list["TxRichText"]
    icon: Optional[Union["NotionEmoji", "NotionFile"]] = None
    color: "TxColor" = None


class TxCode(BaseNotionModel):
    """Represents a code block.

    Attributes:
        caption: The rich text in the caption of the code block.
        rich_text: 	The rich text in the code block.
        language: The language of the code contained in the code block.
    """

    caption: Optional[list["TxRichText"]] = None
    rich_text: list["TxRichText"]
    language: "ProgrammingLanguage"


class TxCaptionHostedFile(BaseNotionModel):
    """Represents a hosted file.

    Attributes:
        type: The type of the file.
        file: The hosted file object.
        caption: The caption of the file.
    """

    type: Literal[FileType.FILE] = FileType.FILE
    file: "HostedFileObject"
    caption: Optional[list["TxRichText"]] = None


class TxCaptionExternalFile(BaseNotionModel):
    """Represents an external file.

    Attributes:
        type: The type of the file.
        external: The URL of the externally hosted file.
        caption: The caption of the file.
    """

    type: Literal[FileType.EXTERNAL] = FileType.EXTERNAL
    external: "ExternalFileObject"
    caption: Optional[list["TxRichText"]] = None


TX_CAPTION_FILE_CLASS_MAP = {
    FileType.FILE: "TxCaptionHostedFile",
    FileType.EXTERNAL: "TxCaptionExternalFile",
}

TxCaptionFile = Annotated[
    Union[tuple(TX_CAPTION_FILE_CLASS_MAP.values())],
    BeforeValidator(lambda v: discriminate_field(v, "type", TX_CAPTION_FILE_CLASS_MAP)),
]


class TxCaptionHostedFileWithName(TxCaptionHostedFile):
    """Represents a hosted file with a name.

    Attributes:
        type: The type of the file.
        file: The hosted file object.
        caption: The caption of the file.
        name: The name of the file.
    """

    name: str


class TxCaptionExternalFileWithName(TxCaptionExternalFile):
    """Represents an external file with a name.

    Attributes:
        type: The type of the file.
        external: The URL of the externally hosted file.
        caption: The caption of the file.
        name: The name of the file.
    """

    name: str


TX_CAPTION_FILE_WITH_NAME_CLASS_MAP = {
    FileType.FILE: "TxCaptionHostedFileWithName",
    FileType.EXTERNAL: "TxCaptionExternalFileWithName",
}

TxCaptionFileWithName = Annotated[
    Union[tuple(TX_CAPTION_FILE_WITH_NAME_CLASS_MAP.values())],
    BeforeValidator(
        lambda v: discriminate_field(v, "type", TX_CAPTION_FILE_WITH_NAME_CLASS_MAP)
    ),
]


class TxHeading(BaseNotionModel):
    """Represents a heading.

    Attributes:
        rich_text: The rich texts in the heading.
        color: The color of the heading.
        is_toggleable: Whether the heading is toggleable.
        children: The nested child blocks.
    """

    rich_text: list["TxRichText"]
    color: "TxColor" = None
    is_toggleable: Optional[bool] = None
    children: Optional[list["TxBlock"]] = None

    @model_validator(mode="after")
    def _validate_properties(self):
        if not self.is_toggleable and self.children:
            raise ValueError("is_toggleable must be True when children are present.")
        return self


class TxNumberedListItem(_TxTextBaseBlockObject):
    """Represents a numbered list item."""

    pass


class TxParagraph(_TxTextBaseBlockObject):
    """Represents a paragraph."""

    pass


class TxQuote(_TxTextBaseBlockObject):
    """Represents a quote."""

    pass


class TxOriginalSynced(BaseNotionModel):
    """Represents an original synced block.

    Attributes:
        synced_from: Always None
        children: The nested child blocks.
    """

    synced_from: None = None
    children: list["TxBlock"] = Field(default_factory=list)

    @model_serializer(mode="wrap")
    def _serialize_model(self, handler):
        data = handler(self, handler)
        if data:
            data["synced_from"] = None
        return data


TxSynced = Annotated[
    Annotated["TxOriginalSynced", Tag("original")]
    | Annotated["DuplicateSynced", Tag("duplicated")],
    Discriminator(model_synced_discriminator),
]


class TxTableRow(BaseNotionModel):
    """Represents the cells of a table.

    Attributes:
        cells: the cells
    """

    cells: list[list["TxRichText"]]


class TxTable(BaseNotionModel):
    """Represents a table.

    Attributes:
        table_width: The number of columns in the table.
        has_column_header: Whether the table has a column header.
        has_row_header: Whether the table has a row header.
    """

    table_width: Annotated[int, Field(gt=0)]
    has_column_header: bool
    has_row_header: bool
    children: list["TxTableRowBlock"]


class TxToDo(_TxTextBaseBlockObject):
    """Represents a to-do.

    Attributes:
        checked: Whether the to-do is checked.
    """

    checked: Optional[bool] = None


class TxToggle(_TxTextBaseBlockObject):
    """Represents a toggle."""

    pass


class TxColumnChildren(BaseNotionModel):
    """Represents the content of a column.

    Attributes:
        children: the children
    """

    children: list["TxBlock"]


class TxColumnBlocks(BaseNotionModel):
    """Represents the columns of a table.

    Attributes:
        children: the columns.
    """

    children: list["TxColumnBlock"]


class _TxBaseBlock(BaseNotionModel):
    """Represents a base block.

    Attributes:
        object: The type of the block.
    """

    object: Literal[NotionObjectType.BLOCK] = NotionObjectType.BLOCK


class TxBookmarkBlock(_TxBaseBlock):
    """Represents a bookmark.

    Attributes:
        type: The type of the block.
        bookmark: The bookmark object.
    """

    type: Literal[BlockType.BOOKMARK] = BlockType.BOOKMARK
    bookmark: "TxBookmark"


class TxBreadcrumbBlock(_TxBaseBlock):
    """Represents a breadcrumb.

    Attributes:
        type: The type of the block.
        breadcrumb: The breadcrumb object
    """

    type: Literal[BlockType.BREADCRUMB] = BlockType.BREADCRUMB
    breadcrumb: "NotionEmptyDict" = Field(default_factory=dict)


class TxBulletListItemBlock(_TxBaseBlock):
    """Represents a bullet list item.

    Attributes:
        type: the type of the block.
        bulleted_list_item: the bullet list item
    """

    type: Literal[BlockType.BULLETED_LIST_ITEM] = BlockType.BULLETED_LIST_ITEM
    bulleted_list_item: "TxBulletListItem"


class TxCalloutBlock(_TxBaseBlock):
    """Represents a callout.

    Attributes:
        type: the type of the block.
        callout: the callout
    """

    type: Literal[BlockType.CALLOUT] = BlockType.CALLOUT
    callout: "TxCallout"


class TxCodeBlock(_TxBaseBlock):
    """Represents a code block.

    Attributes:
        type: the type of the block.
        code: the code.
    """

    type: Literal[BlockType.CODE] = BlockType.CODE
    code: "TxCode"


class TxColumnBlock(_TxBaseBlock):
    """Represents a column block.

    Attributes:
        type: the type of the block.
        column: the column.
    """

    type: Literal[BlockType.COLUMN] = BlockType.COLUMN
    column: "TxColumnChildren"


class TxColumnListBlock(_TxBaseBlock):
    """Represents a column list block.

    Attributes:
        type: the type of the block.
        column_list: the column list.
    """

    type: Literal[BlockType.COLUMN_LIST] = BlockType.COLUMN_LIST
    column_list: "TxColumnBlocks"


class TxDividerBlock(_TxBaseBlock):
    """Represents a divider block.

    Attributes:
        type: the type of the block.
        divider: the divider
    """

    type: Literal[BlockType.DIVIDER] = BlockType.DIVIDER
    divider: "NotionEmptyDict" = Field(default_factory=dict)


class TxEmbedBlock(_TxBaseBlock):
    """Represents an embed block.

    Attributes:
        type: the type of the block.
        embed: the embed
    """

    type: Literal[BlockType.EMBED] = BlockType.EMBED
    embed: "NotionUrlWrapper"


class TxEquationBlock(_TxBaseBlock):
    """Represents an equation block.

    Attributes:
        type: the type of the block.
        equation: the equation
    """

    type: Literal[BlockType.EQUATION] = BlockType.EQUATION
    equation: "NotionEquation"


class TxFileBlock(_TxBaseBlock):
    """Represents a file block.

    Attributes:
        type: the type of the block.
        file: the file
    """

    type: Literal[BlockType.FILE] = BlockType.FILE
    file: TxCaptionFileWithName


class TxHeadingOneBlock(_TxBaseBlock):
    """Represents a heading 1 block.

    Attributes:
        type: the type of the block.
        heading_1: the heading
    """

    type: Literal[BlockType.HEADING_1] = BlockType.HEADING_1
    heading_1: TxHeading


class TxHeadingTwoBlock(_TxBaseBlock):
    """Represents a heading 2 block.

    Attributes:
        type: the type of the block.
        heading_2: the heading
    """

    type: Literal[BlockType.HEADING_2] = BlockType.HEADING_2
    heading_2: TxHeading


class TxHeadingThreeBlock(_TxBaseBlock):
    """Represents a heading 3 block.

    Attributes:
        type: the type of the block.
        heading_3: the heading
    """

    type: Literal[BlockType.HEADING_3] = BlockType.HEADING_3
    heading_3: TxHeading


class TxImageBlock(_TxBaseBlock):
    """Represents an image block.

    Attributes:
        type: the type of the block.
        image: the image
    """

    type: Literal[BlockType.IMAGE] = BlockType.IMAGE
    image: "NotionFile"


class TxNumberedListItemBlock(_TxBaseBlock):
    """Represents a numbered list item block.

    Attributes:
        type: the type of the block.
        numbered_list_item: the numbered list item
    """

    type: Literal[BlockType.NUMBERED_LIST_ITEM] = BlockType.NUMBERED_LIST_ITEM
    numbered_list_item: "TxNumberedListItem"


class TxParagraphBlock(_TxBaseBlock):
    """Represents a paragraph block.

    Attributes:
        type: the type of the block.
        paragraph: the paragraph
    """

    type: Literal[BlockType.PARAGRAPH] = BlockType.PARAGRAPH
    paragraph: "TxParagraph"


class TxPdfBlock(_TxBaseBlock):
    """Represents a PDF block.

    Attributes:
        type: the type of the block.
        pdf: the PDF
    """

    type: Literal[BlockType.PDF] = BlockType.PDF
    pdf: "TxCaptionFile"


class TxQuoteBlock(_TxBaseBlock):
    """Represents a quote block.

    Attributes:
        type: the type of the block.
        quote: the quote
    """

    type: Literal[BlockType.QUOTE] = BlockType.QUOTE
    quote: "TxQuote"


class TxSyncedBlock(_TxBaseBlock):
    """Represents a synced block.

    Attributes:
        type: the type of the block.
        synced_block: the synced block
    """

    type: Literal[BlockType.SYNCED_BLOCK] = BlockType.SYNCED_BLOCK
    synced_block: "TxSynced"


class TxTableBlock(_TxBaseBlock):
    """Represents a table block.

    Attributes:
        type: the type of the block.
        table: the table
    """

    type: Literal[BlockType.TABLE] = BlockType.TABLE
    table: "TxTable"


class TxTableRowBlock(_TxBaseBlock):
    """Represents a table row block.

    Attributes:
        type: the type of the block.
        table_row: the table row
    """

    type: Literal[BlockType.TABLE_ROW] = BlockType.TABLE_ROW
    table_row: "TxTableRow"


class TxTableContentBlock(_TxBaseBlock):
    """Represents a table-of-contents block.

    Attributes:
        type: the type of the block.
        table_of_contents: the table of contents
    """

    type: Literal[BlockType.TABLE_OF_CONTENTS] = BlockType.TABLE_OF_CONTENTS
    table_of_contents: "TableOfContents"


class TxToDoBlock(_TxBaseBlock):
    """Represents a to-do block.

    Attributes:
        type: the type of the block.
        to_do: the to-do
    """

    type: Literal[BlockType.TO_DO] = BlockType.TO_DO
    to_do: "TxToDo"


class TxToggleBlock(_TxBaseBlock):
    """Represents a toggle block.

    Attributes:
        type: the type of the block.
        toggle: the toggle
    """

    type: Literal[BlockType.TOGGLE] = BlockType.TOGGLE
    toggle: "TxToggle"


class TxVideoBlock(_TxBaseBlock):
    """Represents a video block.

    Attributes:
        type: the type of the block.
        video: the video
    """

    type: Literal[BlockType.VIDEO] = BlockType.VIDEO
    video: "TxCaptionFile"


TX_BLOCK_CLASS_MAP = {
    BlockType.BOOKMARK: "TxBookmarkBlock",
    BlockType.BREADCRUMB: "TxBreadcrumbBlock",
    BlockType.BULLETED_LIST_ITEM: "TxBulletListItemBlock",
    BlockType.CALLOUT: "TxCalloutBlock",
    BlockType.CODE: "TxCodeBlock",
    BlockType.COLUMN: "TxColumnBlock",
    BlockType.COLUMN_LIST: "TxColumnListBlock",
    BlockType.DIVIDER: "TxDividerBlock",
    BlockType.EMBED: "TxEmbedBlock",
    BlockType.EQUATION: "TxEquationBlock",
    BlockType.FILE: "TxFileBlock",
    BlockType.HEADING_1: "TxHeadingOneBlock",
    BlockType.HEADING_2: "TxHeadingTwoBlock",
    BlockType.HEADING_3: "TxHeadingThreeBlock",
    BlockType.IMAGE: "TxImageBlock",
    BlockType.NUMBERED_LIST_ITEM: "TxNumberedListItemBlock",
    BlockType.PARAGRAPH: "TxParagraphBlock",
    BlockType.PDF: "TxPdfBlock",
    BlockType.QUOTE: "TxQuoteBlock",
    BlockType.SYNCED_BLOCK: "TxSyncedBlock",
    BlockType.TABLE: "TxTableBlock",
    BlockType.TABLE_ROW: "TxTableRowBlock",
    BlockType.TABLE_OF_CONTENTS: "TxTableContentBlock",
    BlockType.TO_DO: "TxToDoBlock",
    BlockType.TOGGLE: "TxToggleBlock",
    BlockType.VIDEO: "TxVideoBlock",
}

if not TYPE_CHECKING:
    TxBlock = Annotated[
        Union[tuple(TX_BLOCK_CLASS_MAP.values())],
        BeforeValidator(lambda v: discriminate_field(v, "type", TX_BLOCK_CLASS_MAP)),
    ]
else:
    TxBlock = Union[
        TxBookmarkBlock,
        TxBreadcrumbBlock,
        TxBulletListItemBlock,
        TxCalloutBlock,
        TxCodeBlock,
        TxColumnBlock,
        TxColumnListBlock,
        TxDividerBlock,
        TxEmbedBlock,
        TxEquationBlock,
        TxFileBlock,
        TxHeadingOneBlock,
        TxHeadingTwoBlock,
        TxHeadingThreeBlock,
        TxImageBlock,
        TxNumberedListItemBlock,
        TxParagraphBlock,
        TxPdfBlock,
        TxQuoteBlock,
        TxSyncedBlock,
        TxTableBlock,
        TxTableRowBlock,
        TxTableContentBlock,
        TxToDoBlock,
        TxToggleBlock,
        TxVideoBlock,
    ]
