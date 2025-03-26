from __future__ import annotations as _annotations

from enum import Enum
from typing import Literal, Optional, Annotated

from pydantic import Field, BeforeValidator, ConfigDict, Discriminator, Tag

from ._internal import (
    BaseNotionModel,
    FrozenNotionModel,
    validate_url,
    validate_enum,
)
from .emoji import Emoji
from .file import (
    HostedFile,
    ExternalFile,
    File,
    HostedFileWithName,
    ExternalFileWithName,
)
from .object import NotionObjectId, NotionObjectType
from .parent import Parent
from .rich_text import RxRichText, TxRichText
from .types import (
    BackgroundColor,
    Color,
    NotionUrlObject,
    NotionEquation,
    NotionDatetime,
)
from .user import UserRef


class BlockType(str, Enum):
    """Enumeration of block types supported by the Notion API."""

    BOOKMARK = "bookmark"
    BREADCRUMB = "breadcrumb"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    CALLOUT = "callout"
    CHILD_DATABASE = "child_database"
    CHILD_PAGE = "child_page"
    CODE = "code"
    COLUMN = "column"
    COLUMN_LIST = "column_list"
    DIVIDER = "divider"
    EMBED = "embed"
    EQUATION = "equation"
    FILE = "file"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    IMAGE = "image"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    PARAGRAPH = "paragraph"
    PDF = "pdf"
    QUOTE = "quote"
    SYNCED_BLOCK = "synced_block"
    TABLE = "table"
    TABLE_OF_CONTENTS = "table_of_contents"
    TABLE_ROW = "table_row"
    TO_DO = "to_do"
    TOGGLE = "toggle"
    UNSUPPORTED = "unsupported"
    VIDEO = "video"


class ProgrammingLanguage(str, Enum):
    """Enumeration of supported programming languages for Notion code blocks."""

    ABAP = "abap"
    ARDUINO = "arduino"
    BASH = "bash"
    BASIC = "basic"
    C = "c"
    CLOJURE = "clojure"
    COFFEESCRIPT = "coffeescript"
    CPP = "c++"
    CSHARP = "c#"
    CSS = "css"
    DART = "dart"
    DIFF = "diff"
    DOCKER = "docker"
    ELIXIR = "elixir"
    ELM = "elm"
    ERLANG = "erlang"
    FLOW = "flow"
    FORTRAN = "fortran"
    FSHARP = "f#"
    GHERKIN = "gherkin"
    GLSL = "glsl"
    GO = "go"
    GRAPHQL = "graphql"
    GROOVY = "groovy"
    HASKELL = "haskell"
    HTML = "html"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    JSON = "json"
    JULIA = "julia"
    KOTLIN = "kotlin"
    LATEX = "latex"
    LESS = "less"
    LISP = "lisp"
    LIVESCRIPT = "livescript"
    LUA = "lua"
    MAKEFILE = "makefile"
    MARKDOWN = "markdown"
    MARKUP = "markup"
    MATLAB = "matlab"
    MERMAID = "mermaid"
    NIX = "nix"
    OBJECTIVE_C = "objective-c"
    OCAML = "ocaml"
    PASCAL = "pascal"
    PERL = "perl"
    PHP = "php"
    PLAIN_TEXT = "plain text"
    POWERSHELL = "powershell"
    PROLOG = "prolog"
    PROTOBUF = "protobuf"
    PYTHON = "python"
    R = "r"
    REASON = "reason"
    RUBY = "ruby"
    RUST = "rust"
    SASS = "sass"
    SCALA = "scala"
    SCHEME = "scheme"
    SCSS = "scss"
    SHELL = "shell"
    SQL = "sql"
    SWIFT = "swift"
    TYPESCRIPT = "typescript"
    VB_NET = "vb.net"
    VERILOG = "verilog"
    VHDL = "vhdl"
    VISUAL_BASIC = "visual basic"
    WEBASSEMBLY = "webassembly"
    XML = "xml"
    YAML = "yaml"
    JAVA_C_CPP_CSHARP = "java/c/c++/c#"


RxRichTexts = list[RxRichText]
RxCaption = Optional[list[RxRichText]]


class ChildDatabase(BaseNotionModel):
    title: str


class ChildPage(BaseNotionModel):
    title: str


class Table(BaseNotionModel):
    table_width: Annotated[int, Field(gt=0)]
    has_column_header: bool
    has_row_header: bool


class SyncedFrom(BaseNotionModel):
    """Represents the type of the synced from the object.

    Attributes:
        block_id: The synced block.
    """

    block_id: NotionObjectId


class DuplicateSynced(BaseNotionModel):
    synced_from: SyncedFrom
    children: None = None


def model_synced_discriminator(v):

    from ._internal.utils import get_value_for_discriminator

    synced_from_value = get_value_for_discriminator(v, "synced_from")

    if synced_from_value is not None:
        return "duplicated"
    else:
        return "original"


class _RxTextBaseBlockObject(FrozenNotionModel):
    """Represents a text-based block value.

    Attributes:
        rich_text: the rich texts in the block.
        children: the nested child blocks.
        color: the color of the block.
    """

    rich_text: RxRichTexts
    children: Optional[list[RxBlock]]
    color: Color | BackgroundColor


class RxBookmark(FrozenNotionModel):
    caption: RxCaption = None
    url: Annotated[str, BeforeValidator(validate_url)]


class RxBulletListItem(_RxTextBaseBlockObject):
    pass


class RxCallout(FrozenNotionModel):
    rich_text: RxRichTexts
    icon: Optional[Emoji | File]
    color: Color | BackgroundColor


class RxCode(FrozenNotionModel):
    caption: RxCaption = None
    rich_text: RxRichTexts
    language: ProgrammingLanguage


class RxCaptionHostedFile(HostedFile):
    caption: RxCaption = None


class RxCaptionExternalFile(ExternalFile):
    caption: RxCaption = None


RxCaptionFile = Annotated[
    RxCaptionHostedFile | RxCaptionExternalFile, Field(discriminator="type")
]


class RxCaptionHostedFileWithName(HostedFileWithName):
    caption: RxCaption = None


class RxCaptionExternalFileWithName(ExternalFileWithName):
    caption: RxCaption = None


RxCaptionFileWithName = Annotated[
    RxCaptionHostedFileWithName | RxCaptionExternalFileWithName,
    Field(discriminator="type"),
]


class RxHeading(FrozenNotionModel):
    rich_text: RxRichTexts
    color: Color | BackgroundColor
    is_toggleable: bool


class RxNumberedListItem(_RxTextBaseBlockObject):
    pass


class RxParagraph(_RxTextBaseBlockObject):
    pass


class RxQuote(_RxTextBaseBlockObject):
    pass


class RxOriginalSynced(FrozenNotionModel):
    synced_from: None = None
    children: list[RxBlock]


RxSynced = Annotated[
    Annotated[RxOriginalSynced, Tag("original")]
    | Annotated[DuplicateSynced, Tag("duplicated")],
    Discriminator(model_synced_discriminator),
]


class RxCells(FrozenNotionModel):
    rich_text: RxRichTexts


class RxToDo(_RxTextBaseBlockObject):
    checked: bool


class RxToggle(_RxTextBaseBlockObject):
    pass


class _RxBaseBlock(FrozenNotionModel):
    object: Literal[NotionObjectType.BLOCK] = NotionObjectType.BLOCK
    id: NotionObjectId
    parent: Optional[Parent] = None
    created_time: Optional[NotionDatetime] = None
    last_edited_time: Optional[NotionDatetime] = None
    created_by: Optional[UserRef] = None
    last_edited_by: Optional[UserRef] = None
    archived: Optional[bool] = None
    in_trash: Optional[bool] = None
    has_children: Optional[bool] = None


class RxBookmarkBlock(_RxBaseBlock):
    type: Literal[BlockType.BOOKMARK] = Field(default=BlockType.BOOKMARK)
    bookmark: RxBookmark


class RxBreadcrumbBlock(_RxBaseBlock):
    type: Literal[BlockType.BREADCRUMB] = Field(default=BlockType.BREADCRUMB)
    breadcrumb: dict


class RxBulletListItemBlock(_RxBaseBlock):
    type: Literal[BlockType.BULLETED_LIST_ITEM] = Field(
        default=BlockType.BULLETED_LIST_ITEM
    )
    bullet_list_item: RxBulletListItem


class RxCalloutBlock(_RxBaseBlock):
    type: Literal[BlockType.CALLOUT] = Field(default=BlockType.CALLOUT)
    callout: RxCallout


class RxChildDatabaseBlock(_RxBaseBlock):
    type: Literal[BlockType.CHILD_DATABASE] = Field(default=BlockType.CHILD_DATABASE)
    child_database: ChildDatabase


class RxChildPageBlock(_RxBaseBlock):
    type: Literal[BlockType.CHILD_PAGE] = Field(default=BlockType.CHILD_PAGE)
    child_page: ChildPage


class RxCodeBlock(_RxBaseBlock):
    type: Literal[BlockType.CODE] = Field(default=BlockType.CODE)
    code: RxCode


class RxColumnListBlock(_RxBaseBlock):
    type: Literal[BlockType.COLUMN_LIST] = Field(default=BlockType.COLUMN_LIST)
    column_list: dict


class RxColumnBlock(_RxBaseBlock):
    type: Literal[BlockType.COLUMN] = Field(default=BlockType.COLUMN)
    column: dict


class RxDividerBlock(_RxBaseBlock):
    type: Literal[BlockType.DIVIDER] = Field(default=BlockType.DIVIDER)
    divider: dict


class RxEmbedBlock(_RxBaseBlock):
    type: Literal[BlockType.EMBED] = Field(default=BlockType.EMBED)
    embed: NotionUrlObject


class RxEquationBlock(_RxBaseBlock):
    type: Literal[BlockType.EQUATION] = Field(default=BlockType.EQUATION)
    equation: NotionEquation


class RxFileBlock(_RxBaseBlock):
    type: Literal[BlockType.FILE] = Field(default=BlockType.FILE)
    file: RxCaptionFileWithName


class RxHeadingOneBlock(_RxBaseBlock):
    type: Literal[BlockType.HEADING_1] = Field(default=BlockType.HEADING_1)
    heading_1: RxHeading


class RxHeadingTwoBlock(_RxBaseBlock):
    type: Literal[BlockType.HEADING_2] = Field(default=BlockType.HEADING_2)
    heading_2: RxHeading


class RxHeadingThreeBlock(_RxBaseBlock):
    type: Literal[BlockType.HEADING_3] = Field(default=BlockType.HEADING_3)
    heading_3: RxHeading


class RxImageBlock(_RxBaseBlock):
    type: Literal[BlockType.IMAGE] = Field(default=BlockType.IMAGE)
    image: File


class RxNumberedListItemBlock(_RxBaseBlock):
    type: Literal[BlockType.NUMBERED_LIST_ITEM] = Field(
        default=BlockType.NUMBERED_LIST_ITEM
    )
    numbered_list_item: RxNumberedListItem


class RxParagraphBlock(_RxBaseBlock):
    type: Literal[BlockType.PARAGRAPH] = Field(default=BlockType.PARAGRAPH)
    paragraph: RxParagraph


class RxPdfBlock(_RxBaseBlock):
    type: Literal[BlockType.PDF] = Field(default=BlockType.PDF)
    pdf: RxCaptionFile


class RxQuoteBlock(_RxBaseBlock):
    type: Literal[BlockType.QUOTE] = Field(default=BlockType.QUOTE)
    quote: RxQuote


class RxSyncedBlock(_RxBaseBlock):
    type: Literal[BlockType.SYNCED_BLOCK] = Field(default=BlockType.SYNCED_BLOCK)
    synced_block: RxSynced


class RxTableBlock(_RxBaseBlock):
    type: Literal[BlockType.TABLE] = Field(default=BlockType.TABLE)
    table: Table


class RxTableRowBlock(_RxBaseBlock):
    type: Literal[BlockType.TABLE_ROW] = Field(default=BlockType.TABLE_ROW)
    table_row: RxCells


class RxTableContentBlock(_RxBaseBlock):
    type: Literal[BlockType.TABLE_OF_CONTENTS] = Field(
        default=BlockType.TABLE_OF_CONTENTS
    )
    table_of_contents: Color | BackgroundColor


class RxToDoBlock(_RxBaseBlock):
    type: Literal[BlockType.TO_DO] = Field(default=BlockType.TO_DO)
    to_do: RxToDo


class RxToggleBlock(_RxBaseBlock):
    type: Literal[BlockType.TOGGLE] = Field(default=BlockType.TOGGLE)
    toggle: RxToggle


class RxVideoBlock(_RxBaseBlock):
    type: Literal[BlockType.VIDEO] = Field(default=BlockType.VIDEO)
    video: RxCaptionFile


class RxUnsupportedBlock(_RxBaseBlock):
    model_config = ConfigDict(
        extra="allow", populate_by_name=True, arbitrary_types_allowed=True, frozen=True
    )

    type: Literal[BlockType.UNSUPPORTED] = Field(default=BlockType.UNSUPPORTED)
    unsupported: dict


RxBlock = Annotated[
    RxBookmarkBlock
    | RxBreadcrumbBlock
    | RxBulletListItemBlock
    | RxCalloutBlock
    | RxChildDatabaseBlock
    | RxChildPageBlock
    | RxCodeBlock
    | RxColumnBlock
    | RxColumnListBlock
    | RxDividerBlock
    | RxEmbedBlock
    | RxEquationBlock
    | RxFileBlock
    | RxHeadingOneBlock
    | RxHeadingTwoBlock
    | RxHeadingThreeBlock
    | RxImageBlock
    | RxNumberedListItemBlock
    | RxParagraphBlock
    | RxPdfBlock
    | RxQuoteBlock
    | RxSyncedBlock
    | RxTableBlock
    | RxTableRowBlock
    | RxTableContentBlock
    | RxToDoBlock
    | RxToggleBlock
    | RxVideoBlock
    | RxUnsupportedBlock,
    Field(discriminator="type"),
]

TxRichTexts = list[TxRichText]
TxCaption = Optional[list[TxRichText]]

TxColor = Optional[
    Annotated[
        str | Color | BackgroundColor,
        BeforeValidator(lambda v: validate_enum(v, (Color, BackgroundColor))),
    ]
]


class _TxTextBaseBlockObject(BaseNotionModel):
    """Represents a text-based block value.

    Attributes:
        rich_text: the rich texts in the block.
        children: the nested child blocks.
        color: the color of the block.
    """

    rich_text: TxRichTexts = Field(default_factory=list)
    children: Optional[list[TxBlock]] = None
    color: TxColor = None


class TxBookmark(BaseNotionModel):
    caption: TxCaption = None
    url: Annotated[str, BeforeValidator(validate_url)]


class TxBulletListItem(_TxTextBaseBlockObject):
    pass


class TxCallout(BaseNotionModel):
    rich_text: TxRichTexts
    icon: Optional[Emoji | File] = None
    color: TxColor = None


class TxCode(BaseNotionModel):
    caption: TxCaption = None
    rich_text: TxRichTexts
    language: ProgrammingLanguage


class TxCaptionHostedFile(HostedFile):
    caption: TxCaption = None


class TxCaptionExternalFile(ExternalFile):
    caption: TxCaption = None


TxCaptionFile = Annotated[
    TxCaptionHostedFile | TxCaptionExternalFile, Field(discriminator="type")
]


class TxCaptionHostedFileWithName(HostedFileWithName):
    caption: TxCaption = None


class TxCaptionExternalFileWithName(ExternalFileWithName):
    caption: TxCaption = None


TxCaptionFileWithName = Annotated[
    TxCaptionHostedFileWithName | TxCaptionExternalFileWithName,
    Field(discriminator="type"),
]


class TxHeading(BaseNotionModel):
    rich_text: TxRichTexts
    color: TxColor = None
    is_toggleable: Optional[bool] = None


class TxNumberedListItem(_TxTextBaseBlockObject):
    pass


class TxParagraph(_TxTextBaseBlockObject):
    pass


class TxQuote(_TxTextBaseBlockObject):
    pass


class TxOriginalSynced(BaseNotionModel):
    synced_from: None = None
    children: list[TxBlock] = Field(default_factory=list)


TxSynced = Annotated[
    Annotated[TxOriginalSynced, Tag("original")]
    | Annotated[DuplicateSynced, Tag("duplicated")],
    Discriminator(model_synced_discriminator),
]


class TxCells(BaseNotionModel):
    rich_text: TxRichTexts


class TxToDo(_TxTextBaseBlockObject):
    checked: Optional[bool] = None


class TxToggle(_TxTextBaseBlockObject):
    pass


class _TxBaseBlock(BaseNotionModel):
    object: Literal[NotionObjectType.BLOCK] = NotionObjectType.BLOCK


class TxBookmarkBlock(_TxBaseBlock):
    type: Literal[BlockType.BOOKMARK] = BlockType.BOOKMARK
    bookmark: TxBookmark


class TxBreadcrumbBlock(_TxBaseBlock):
    type: Literal[BlockType.BREADCRUMB] = Field(default=BlockType.BREADCRUMB)
    breadcrumb: dict = Field(default_factory=dict)


class TxBulletListItemBlock(_TxBaseBlock):
    type: Literal[BlockType.BULLETED_LIST_ITEM] = Field(
        default=BlockType.BULLETED_LIST_ITEM
    )
    bullet_list_item: TxBulletListItem


class TxCalloutBlock(_TxBaseBlock):
    type: Literal[BlockType.CALLOUT] = Field(default=BlockType.CALLOUT)
    callout: TxCallout


class TxChildDatabaseBlock(_TxBaseBlock):
    type: Literal[BlockType.CHILD_DATABASE] = Field(default=BlockType.CHILD_DATABASE)
    child_database: ChildDatabase


class TxChildPageBlock(_TxBaseBlock):
    type: Literal[BlockType.CHILD_PAGE] = Field(default=BlockType.CHILD_PAGE)
    child_page: ChildPage


class TxCodeBlock(_TxBaseBlock):
    type: Literal[BlockType.CODE] = Field(default=BlockType.CODE)
    code: TxCode


class TxColumnListBlock(_TxBaseBlock):
    type: Literal[BlockType.COLUMN_LIST] = Field(default=BlockType.COLUMN_LIST)
    column_list: dict = Field(default_factory=dict)


class TxColumnBlock(_TxBaseBlock):
    type: Literal[BlockType.COLUMN] = Field(default=BlockType.COLUMN)
    column: dict = Field(default_factory=dict)


class TxDividerBlock(_TxBaseBlock):
    type: Literal[BlockType.DIVIDER] = Field(default=BlockType.DIVIDER)
    divider: dict = Field(default_factory=dict)


class TxEmbedBlock(_TxBaseBlock):
    type: Literal[BlockType.EMBED] = Field(default=BlockType.EMBED)
    embed: NotionUrlObject


class TxEquationBlock(_TxBaseBlock):
    type: Literal[BlockType.EQUATION] = Field(default=BlockType.EQUATION)
    equation: NotionEquation


class TxFileBlock(_TxBaseBlock):
    type: Literal[BlockType.FILE] = Field(default=BlockType.FILE)
    file: TxCaptionFileWithName


class TxHeadingOneBlock(_TxBaseBlock):
    type: Literal[BlockType.HEADING_1] = Field(default=BlockType.HEADING_1)
    heading_1: TxHeading


class TxHeadingTwoBlock(_TxBaseBlock):
    type: Literal[BlockType.HEADING_2] = Field(default=BlockType.HEADING_2)
    heading_2: TxHeading


class TxHeadingThreeBlock(_TxBaseBlock):
    type: Literal[BlockType.HEADING_3] = Field(default=BlockType.HEADING_3)
    heading_3: TxHeading


class TxImageBlock(_TxBaseBlock):
    type: Literal[BlockType.IMAGE] = Field(default=BlockType.IMAGE)
    image: File


class TxNumberedListItemBlock(_TxBaseBlock):
    type: Literal[BlockType.NUMBERED_LIST_ITEM] = Field(
        default=BlockType.NUMBERED_LIST_ITEM
    )
    numbered_list_item: TxNumberedListItem


class TxParagraphBlock(_TxBaseBlock):
    type: Literal[BlockType.PARAGRAPH] = Field(default=BlockType.PARAGRAPH)
    paragraph: TxParagraph


class TxPdfBlock(_TxBaseBlock):
    type: Literal[BlockType.PDF] = Field(default=BlockType.PDF)
    pdf: TxCaptionFile


class TxQuoteBlock(_TxBaseBlock):
    type: Literal[BlockType.QUOTE] = Field(default=BlockType.QUOTE)
    quote: TxQuote


class TxSyncedBlock(_TxBaseBlock):
    type: Literal[BlockType.SYNCED_BLOCK] = Field(default=BlockType.SYNCED_BLOCK)
    synced_block: TxSynced


class TxTableBlock(_TxBaseBlock):
    type: Literal[BlockType.TABLE] = Field(default=BlockType.TABLE)
    table: Table


class TxTableRowBlock(_TxBaseBlock):
    type: Literal[BlockType.TABLE_ROW] = Field(default=BlockType.TABLE_ROW)
    table_row: TxCells


class TxTableContentBlock(_TxBaseBlock):
    type: Literal[BlockType.TABLE_OF_CONTENTS] = Field(
        default=BlockType.TABLE_OF_CONTENTS
    )
    table_of_contents: TxColor


class TxToDoBlock(_TxBaseBlock):
    type: Literal[BlockType.TO_DO] = Field(default=BlockType.TO_DO)
    to_do: TxToDo


class TxToggleBlock(_TxBaseBlock):
    type: Literal[BlockType.TOGGLE] = Field(default=BlockType.TOGGLE)
    toggle: TxToggle


class TxVideoBlock(_TxBaseBlock):
    type: Literal[BlockType.VIDEO] = Field(default=BlockType.VIDEO)
    video: TxCaptionFile


TxBlock = Annotated[
    TxBookmarkBlock
    | TxBreadcrumbBlock
    | TxBulletListItemBlock
    | TxCalloutBlock
    | TxChildDatabaseBlock
    | TxChildPageBlock
    | TxCodeBlock
    | TxColumnBlock
    | TxColumnListBlock
    | TxDividerBlock
    | TxEmbedBlock
    | TxEquationBlock
    | TxFileBlock
    | TxHeadingOneBlock
    | TxHeadingTwoBlock
    | TxHeadingThreeBlock
    | TxImageBlock
    | TxNumberedListItemBlock
    | TxParagraphBlock
    | TxPdfBlock
    | TxQuoteBlock
    | TxSyncedBlock
    | TxTableBlock
    | TxTableRowBlock
    | TxTableContentBlock
    | TxToDoBlock
    | TxToggleBlock
    | TxVideoBlock,
    Field(discriminator="type"),
]
