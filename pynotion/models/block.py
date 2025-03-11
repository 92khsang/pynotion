from __future__ import annotations as _annotations

from abc import ABC
from enum import StrEnum
from typing import Union, Annotated, TypeAlias, Literal, TypeVar, Generic, Any

from pydantic import Field, model_validator, BeforeValidator, ConfigDict, BaseModel

from ._internal import (
    TypeObjectModel,
    BaseNotionModel,
    validate_enum,
)
from .rich_text import TxRichText, RxRichText
from .types import (
    Color,
    BackgroundColor,
    NotionUrl as _NotionUrl,
    NotionEquation as _NotionEquation,
    NotionFile as _NotionFile,
    NotionEmoji as _NotionEmoji,
    NotionLink as _NotionLink,
    NotionObjectRef as _NotionObjectRef,
    NotionDate as _NotionDate,
    NotionUserRef as _NotionUserRef,
    NotionObjectId as _NotionObjectId,
    RxNotionObject as _RxNotionObject,
    TxNotionObject as _TxNotionObject,
)


class BlockType(StrEnum):
    """Enumeration of block types supported by the Notion API.

    This enum represents all available block types that can be created, retrieved, or
    updated through the Notion API. Each block type corresponds to a specific content
    structure that can be rendered in Notion pages.

    Attributes:
        BOOKMARK: A bookmark block that displays a link with a preview.
        BREADCRUMB: A breadcrumb navigation block showing page hierarchy.
        BULLETED_LIST_ITEM: An item in a bulleted (unordered) list.
        CALLOUT: A callout block with an icon and background, used to highlight content.
        CHILD_DATABASE: A database embedded within a page.
        CHILD_PAGE: A page embedded within another page.
        CODE: A code block with syntax highlighting for various programming languages.
        COLUMN: A single column within a column list block.
        COLUMN_LIST: A container block that holds multiple columns in a row.
        DATABASE: A top-level database object.
        DATE: A date or datetime block.
        DIVIDER: A horizontal divider line to separate content.
        EMBED: An embedded external resource (website, video, etc.).
        EQUATION: A block displaying a mathematical equation using LaTeX.
        FILE: An uploaded file.
        HEADING_1: A large heading (H1).
        HEADING_2: A medium heading (H2).
        HEADING_3: A small heading (H3).
        IMAGE: An image block.
        LINK_PREVIEW: A preview of a linked website or resource.
        NUMBERED_LIST_ITEM: An item in a numbered (ordered) list.
        PAGE: A top-level page object.
        PARAGRAPH: A basic text block.
        PDF: A PDF file viewer.
        QUOTE: A block for quoted text with special formatting.
        SYNCED_BLOCK: A block that can be synced across multiple pages.
        TABLE: A table block containing rows and cells.
        TABLE_OF_CONTENTS: An auto-generated table of contents.
        TABLE_ROW: A row within a table.
        TO_DO: A task with a checkbox.
        TOGGLE: A collapsible toggle block.
        UNSUPPORTED: A block type not currently supported by the API.
        USER: A user mention.
        VIDEO: A video block.
    """

    BOOKMARK = "bookmark"
    BREADCRUMB = "breadcrumb"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    CALLOUT = "callout"
    CHILD_DATABASE = "child_database"
    CHILD_PAGE = "child_page"
    CODE = "code"
    COLUMN = "column"
    COLUMN_LIST = "column_list"
    DATABASE = "database"
    DATE = "date"
    DIVIDER = "divider"
    EMBED = "embed"
    EQUATION = "equation"
    FILE = "file"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    IMAGE = "image"
    LINK_PREVIEW = "link_preview"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    PAGE = "page"
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
    USER = "user"
    VIDEO = "video"


class ProgrammingLanguage(StrEnum):
    """Enumeration of supported programming languages for Notion code blocks.

    This enum provides all programming languages officially supported for syntax
    highlighting in Notion code blocks. The string value of each enum member matches
    exactly with the expected language identifier in the Notion API.

    Attributes:
        ABAP: ABAP programming language.
        ARDUINO: Arduino programming language.
        BASH: Bash shell scripting language.
        BASIC: BASIC programming language.
        C: C programming language.
        CLOJURE: Clojure programming language.
        COFFEESCRIPT: CoffeeScript programming language.
        CPP: C++ programming language.
        CSHARP: C# programming language.
        CSS: Cascading Style Sheets language.
        DART: Dart programming language.
        DIFF: Diff/patch file format.
        DOCKER: Dockerfile format.
        ELIXIR: Elixir programming language.
        ELM: Elm programming language.
        ERLANG: Erlang programming language.
        FLOW: Flow static type checker for JavaScript.
        FORTRAN: Fortran programming language.
        FSHARP: F# programming language.
        GHERKIN: Gherkin language for behavior-driven development.
        GLSL: OpenGL Shading Language.
        GO: Go programming language.
        GRAPHQL: GraphQL query language.
        GROOVY: Groovy programming language.
        HASKELL: Haskell programming language.
        HTML: HTML markup language.
        JAVA: Java programming language.
        JAVASCRIPT: JavaScript programming language.
        JSON: JSON data format.
        JULIA: Julia programming language.
        KOTLIN: Kotlin programming language.
        LATEX: LaTeX document preparation system.
        LESS: Less CSS preprocessor.
        LISP: Lisp programming language.
        LIVESCRIPT: LiveScript programming language.
        LUA: Lua programming language.
        MAKEFILE: Makefile format.
        MARKDOWN: Markdown markup language.
        MARKUP: Generic markup language.
        MATLAB: MATLAB programming language.
        MERMAID: Mermaid diagram syntax.
        NIX: Nix expression language.
        OBJECTIVE_C: Objective-C programming language.
        OCAML: OCaml programming language.
        PASCAL: Pascal programming language.
        PERL: Perl programming language.
        PHP: PHP programming language.
        PLAIN_TEXT: Plain text with no syntax highlighting.
        POWERSHELL: PowerShell scripting language.
        PROLOG: Prolog programming language.
        PROTOBUF: Protocol Buffers format.
        PYTHON: Python programming language.
        R: R programming language.
        REASON: ReasonML programming language.
        RUBY: Ruby programming language.
        RUST: Rust programming language.
        SASS: Sass CSS preprocessor.
        SCALA: Scala programming language.
        SCHEME: Scheme programming language.
        SCSS: SCSS CSS preprocessor.
        SHELL: Generic shell scripting.
        SQL: SQL query language.
        SWIFT: Swift programming language.
        TYPESCRIPT: TypeScript programming language.
        VB_NET: VB.NET programming language.
        VERILOG: Verilog hardware description language.
        VHDL: VHDL hardware description language.
        VISUAL_BASIC: Visual Basic programming language.
        WEBASSEMBLY: WebAssembly format.
        XML: XML markup language.
        YAML: YAML data format.
        JAVA_C_CPP_CSHARP: Generic highlight for Java/C/C++/C# family.
    """

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


RichTextT = TypeVar('RichTextT')
BlockT = TypeVar('BlockT')

BookmarkUrl: TypeAlias = _NotionUrl
CalloutIcon: TypeAlias = _NotionEmoji | _NotionFile
EmbeddedUrl: TypeAlias = _NotionUrl
BlockId: TypeAlias = _NotionObjectId


# --------------------------- Reusable Blocks -------------------------------------
class _EmptyBlock(BaseNotionModel):
    pass


class _TextBaseBlock(BaseNotionModel, Generic[RichTextT, BlockT]):
    """Represents a text-based block.

    Attributes:
        rich_text: The content of the text block.
        color: The color of the text block.
        children: The children of the text block.
    """

    rich_text: list[RichTextT] = Field(default_factory=list)

    color: Color | BackgroundColor = Field(default=Color.DEFAULT)

    children: list[BlockT] = Field(default_factory=list)


class _ChildObjectBlock(BaseNotionModel):
    """Represents a child page or database block.

    Attributes:
        title: The title of the child page or database.
    """

    title: str


# --------------------------- Specific Blocks -------------------------------------
class _BookmarkBlock(BaseNotionModel, Generic[RichTextT]):
    """Represents a bookmark block.

    Attributes:
        url: The URL of the bookmark.
        caption: The caption of the bookmark.
    """

    url: BookmarkUrl

    caption: list[RichTextT]


class _HeadingBlock(BaseNotionModel, Generic[RichTextT]):
    """Represents a heading block.

    Attributes:
        rich_text: The text of the heading block.
        color: The color of the heading block.
        is_toggleable: Whether the heading block is toggleable.
    """

    rich_text: list[RichTextT] = Field(default_factory=list)

    color: Color | BackgroundColor = Field(default=Color.DEFAULT)

    is_toggleable: bool


class _CalloutBlock(BaseNotionModel, Generic[RichTextT]):
    """Represents a callout block.

    Attributes:
        rich_text: The content of the callout.
        icon: The icon of the callout.
        color: The color of the callout.
    """

    rich_text: list[RichTextT] = Field(default_factory=list)

    icon: CalloutIcon

    color: Color | BackgroundColor = Field(default=Color.DEFAULT)


class _CodeBlock(BaseNotionModel, Generic[RichTextT]):
    """Represents a code block.

    Attributes:
        caption: The caption of the code block.
        rich_text: The text of the code block.
        language: The language of the code block.
    """

    caption: list[RichTextT] = Field(default_factory=list)

    rich_text: list[RichTextT] = Field(default_factory=list)

    language: ProgrammingLanguage


class _FileBlock(_NotionFile, Generic[RichTextT]):
    """Represents a file block.

    Attributes:
        caption: The caption of the file block.
        name: The name of the file block.
    """

    caption: list[RichTextT] = Field(default_factory=list)

    name: str


class _PdfBlock(_NotionFile, Generic[RichTextT]):
    """Represents a PDF block.

    Attributes:
        caption: The caption of the PDF block.
    """

    caption: list[RichTextT] = Field(default_factory=list)


class _ToDoBlock(_TextBaseBlock[RichTextT, BlockT], Generic[RichTextT, BlockT]):
    """Represents a to-do block.

    Attributes:
        checked: Whether the 'To do' is checked.
    """

    checked: bool | None = Field(default=None)


class SyncedFrom(BaseNotionModel):
    """Represents the type of the synced from the object.

    Attributes:
        block_id: The synced block.
    """

    block_id: BlockId


class SyncedBlock(BaseNotionModel):
    """Represents a synced block.

    Attributes:
        synced_from: The type of the synced from the object.
        children: The nested child blocks, if any, of the synced_block.
    """

    synced_from: SyncedFrom | None = Field(default=None)

    children: list[RxBlock] | None = Field(default=None)

    @model_validator(mode="after")
    @classmethod
    def check_exclusive_presence(cls, values):
        synced_from, children = values.synced_from, values.children
        if (synced_from is None and children is None) or (
            synced_from is not None and children is not None
        ):
            raise ValueError(
                "Exactly one of 'synced_from' or 'children' must be provided."
            )
        return values


class EmbedBlock(BaseNotionModel):
    """Represents an embed block.

    Attributes:
        url: The URL of the embed.
    """

    url: EmbeddedUrl


class TableBlock(BaseNotionModel):
    """Represents a table block.

    Attributes:
        table_width: The number of columns in the table.
        has_column_header: Whether the table has a column header.
        has_row_header: Whether the table has a header row.
    """

    table_width: Annotated[int, Field(ge=1)]

    has_column_header: bool

    has_row_header: bool


class TableRowBlock(BaseNotionModel):
    """Represents a table row block.

    Attributes:
        cells: An array of cell contents in horizontal display order. Each cell is an array of rich text objects.
    """

    cells: list[TxRichText | RxRichText] = Field(default_factory=list)


class TableContentBlock(BaseNotionModel):
    """Represents a table of contents blocks.


    Attributes:
        color: The color of the table of contents blocks.
    """

    color: Color | BackgroundColor = Field(default=Color.DEFAULT)


class UnsupportedBlock(BaseModel):
    model_config = ConfigDict()


BreadcrumbBlock: TypeAlias = _EmptyBlock

TxBulletedListItemBlock: TypeAlias = _TextBaseBlock["TxRichText", "TxBlock"]
RxBulletedListItemBlock: TypeAlias = _TextBaseBlock["RxRichText", "RxBlock"]

ChildDatabaseBlock: TypeAlias = _ChildObjectBlock
ChildPageBlock: TypeAlias = _ChildObjectBlock

TxBookmarkBlock: TypeAlias = _BookmarkBlock["TxRichText"]
RxBookmarkBlock: TypeAlias = _BookmarkBlock["RxRichText"]

TxHeadingBlock: TypeAlias = _HeadingBlock["TxRichText"]
RxHeadingBlock: TypeAlias = _HeadingBlock["RxRichText"]

TxCalloutBlock: TypeAlias = _CalloutBlock["TxRichText"]
RxCalloutBlock: TypeAlias = _CalloutBlock["RxRichText"]

TxCodeBlock: TypeAlias = _CodeBlock["TxRichText"]
RxCodeBlock: TypeAlias = _CodeBlock["RxRichText"]

TxColumnBlock: TypeAlias = _TextBaseBlock["TxRichText", "TxBlock"]
RxColumnBlock: TypeAlias = _TextBaseBlock["RxRichText", "RxBlock"]

TxColumnListBlock: TypeAlias = _TextBaseBlock["TxRichText", "TxBlock"]
RxColumnListBlock: TypeAlias = _TextBaseBlock["RxRichText", "RxBlock"]

DividerBlock: TypeAlias = _EmptyBlock
EquationBlock: TypeAlias = _NotionEquation

TxFileBlock: TypeAlias = _FileBlock["TxRichText"]
RxFileBlock: TypeAlias = _FileBlock["RxRichText"]
TxImageBlock: TypeAlias = _FileBlock["TxRichText"]
RxImageBlock: TypeAlias = _FileBlock["RxRichText"]
TxPdfBlock: TypeAlias = _PdfBlock["TxRichText"]
RxPdfBlock: TypeAlias = _PdfBlock["RxRichText"]

LinkPreviewBlock: TypeAlias = _NotionLink
MentionDatabaseBlock: TypeAlias = _NotionObjectRef
MentionDateBlock: TypeAlias = _NotionDate
MentionPageBlock: TypeAlias = _NotionObjectRef
MentionUserBlock: TypeAlias = _NotionUserRef

TxNumberedListItemBlock: TypeAlias = _TextBaseBlock["TxRichText", "TxBlock"]
RxNumberedListItemBlock: TypeAlias = _TextBaseBlock["RxRichText", "RxBlock"]

TxParagraphBlock: TypeAlias = _TextBaseBlock["TxRichText", "TxBlock"]
RxParagraphBlock: TypeAlias = _TextBaseBlock["RxRichText", "RxBlock"]

TxQuoteBlock: TypeAlias = _TextBaseBlock["TxRichText", "TxBlock"]
RxQuoteBlock: TypeAlias = _TextBaseBlock["RxRichText", "RxBlock"]

TxToggleBlock: TypeAlias = _TextBaseBlock["TxRichText", "TxBlock"]
RxToggleBlock: TypeAlias = _TextBaseBlock["RxRichText", "RxBlock"]

TxToDoBlock: TypeAlias = _ToDoBlock["TxRichText", "TxBlock"]
RxToDoBlock: TypeAlias = _ToDoBlock["RxRichText", "RxBlock"]

VideoBlock: TypeAlias = _NotionFile


_BaseBlockTypeObjects = Union[
    BreadcrumbBlock,
    ChildDatabaseBlock,
    ChildPageBlock,
    DividerBlock,
    EmbedBlock,
    EquationBlock,
    MentionDatabaseBlock,
    MentionDateBlock,
    MentionPageBlock,
    MentionUserBlock,
    TableBlock,
    TableContentBlock,
    TableRowBlock,
    UnsupportedBlock,
    VideoBlock,
]


class BaseBlock(TypeObjectModel, ABC):
    __type_object_map__ = {
        BlockType.BREADCRUMB: BreadcrumbBlock,
        BlockType.CHILD_DATABASE: ChildDatabaseBlock,
        BlockType.CHILD_PAGE: ChildPageBlock,
        BlockType.DATABASE: MentionDatabaseBlock,
        BlockType.DATE: MentionDateBlock,
        BlockType.DIVIDER: DividerBlock,
        BlockType.EMBED: EmbedBlock,
        BlockType.EQUATION: EquationBlock,
        BlockType.PAGE: MentionPageBlock,
        BlockType.TABLE: TableBlock,
        BlockType.TABLE_ROW: TableRowBlock,
        BlockType.TABLE_OF_CONTENTS: TableContentBlock,
        BlockType.USER: MentionUserBlock,
        BlockType.VIDEO: VideoBlock,
        BlockType.UNSUPPORTED: UnsupportedBlock,
    }

    object: Literal["block"] = Field(frozen=True)

    type: (
        Annotated[str, BeforeValidator(lambda v: validate_enum(v, (BlockType,)))]
        | BlockType
    ) = Field(frozen=True)

    type_object: Any

    @model_validator(mode="before")
    def validate_abstract_clz(cls, values: Any) -> Any:
        if cls is BaseBlock:
            raise TypeError("Cannot instantiate abstract class BaseBlock")

        return values


class TxBlock(_TxNotionObject, BaseBlock):
    """Represents a Notion block for request.

    Attributes:
        object: Always 'block', ensuring consistency.
        type: The type of the block.
        type_object: An object containing type-specific block information.
    """

    __type_object_map__ = {
        **BaseBlock.__type_object_map__,
        BlockType.BOOKMARK: TxBookmarkBlock,
        BlockType.BULLETED_LIST_ITEM: TxBulletedListItemBlock,
        BlockType.CALLOUT: TxCalloutBlock,
        BlockType.CODE: TxCodeBlock,
        BlockType.COLUMN: TxColumnBlock,
        BlockType.COLUMN_LIST: TxColumnListBlock,
        BlockType.FILE: TxFileBlock,
        BlockType.HEADING_1: TxHeadingBlock,
        BlockType.HEADING_2: TxHeadingBlock,
        BlockType.HEADING_3: TxHeadingBlock,
        BlockType.IMAGE: TxImageBlock,
        BlockType.NUMBERED_LIST_ITEM: TxNumberedListItemBlock,
        BlockType.PARAGRAPH: TxParagraphBlock,
        BlockType.PDF: TxPdfBlock,
        BlockType.QUOTE: TxQuoteBlock,
        BlockType.TOGGLE: TxToggleBlock,
        BlockType.TO_DO: TxToDoBlock,
    }

    type_object: Union[
        _BaseBlockTypeObjects,
        TxBookmarkBlock,
        TxBulletedListItemBlock,
        TxCalloutBlock,
        TxCodeBlock,
        TxColumnBlock,
        TxColumnListBlock,
        TxFileBlock,
        TxHeadingBlock,
        TxImageBlock,
        TxNumberedListItemBlock,
        TxParagraphBlock,
        TxPdfBlock,
        TxQuoteBlock,
        TxToDoBlock,
        TxToggleBlock,
    ]


class RxBlock(_RxNotionObject, BaseBlock):
    """Represents a Notion block for response.

    Attributes:
        object: Always 'block', ensuring consistency.
        id: The unique identifier for the object.
        parent: The parent object that contains this object.
        created_time: The timestamp when the object was created.
        last_edited_time: The timestamp when the object was last edited.
        created_by: The user who created the object.
        last_edited_by: The user who last edited the object.
        archived: Whether the object is archived.
        in_trash: Whether the object is in the trash.
        type: The type of the block.
        type_object: An object containing type-specific block information.
        has_children: Whether the block has children.
    """

    __type_object_map__ = {
        **BaseBlock.__type_object_map__,
        BlockType.LINK_PREVIEW: LinkPreviewBlock,
        BlockType.SYNCED_BLOCK: SyncedBlock,
        BlockType.BOOKMARK: RxBookmarkBlock,
        BlockType.BULLETED_LIST_ITEM: RxBulletedListItemBlock,
        BlockType.CALLOUT: RxCalloutBlock,
        BlockType.CODE: RxCodeBlock,
        BlockType.COLUMN: RxColumnBlock,
        BlockType.COLUMN_LIST: RxColumnListBlock,
        BlockType.FILE: RxFileBlock,
        BlockType.HEADING_1: RxHeadingBlock,
        BlockType.HEADING_2: RxHeadingBlock,
        BlockType.HEADING_3: RxHeadingBlock,
        BlockType.IMAGE: RxImageBlock,
        BlockType.NUMBERED_LIST_ITEM: RxNumberedListItemBlock,
        BlockType.PARAGRAPH: RxParagraphBlock,
        BlockType.PDF: RxPdfBlock,
        BlockType.QUOTE: RxQuoteBlock,
        BlockType.TOGGLE: RxToggleBlock,
        BlockType.TO_DO: RxToDoBlock,
    }

    type_object: Union[
        _BaseBlockTypeObjects,
        LinkPreviewBlock,
        SyncedBlock,
        RxBookmarkBlock,
        RxBulletedListItemBlock,
        RxCalloutBlock,
        RxCodeBlock,
        RxColumnBlock,
        RxColumnListBlock,
        RxFileBlock,
        RxHeadingBlock,
        RxImageBlock,
        RxNumberedListItemBlock,
        RxParagraphBlock,
        RxPdfBlock,
        RxQuoteBlock,
        RxToDoBlock,
        RxToggleBlock,
    ] = Field(frozen=True)

    has_children: bool = Field(frozen=True)


Block: TypeAlias = TxBlock | RxBlock
