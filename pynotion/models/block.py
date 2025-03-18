from __future__ import annotations as _annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal, Optional, Annotated

from pydantic import Field, BeforeValidator, ConfigDict

from ._internal import BaseNotionModel, validate_datetime, validate_url
from .emoji import Emojis
from .file import (
    HostedFile,
    ExternalFile,
    File,
    HostedFileWithName,
    ExternalFileWithName,
)
from .object import NotionObjectId, NotionObjectType
from .parent import Parent
from .rich_text import RichText
from .types import BackgroundColor, Color, NotionUrlObject, NotionEquation
from .user import UserRef


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
        DIVIDER: A horizontal divider line to separate content.
        EMBED: An embedded external resource (website, video, etc.).
        EQUATION: A block displaying a mathematical equation using LaTeX.
        FILE: An uploaded file.
        HEADING_1: A large heading (H1).
        HEADING_2: A medium heading (H2).
        HEADING_3: A small heading (H3).
        IMAGE: An image block.
        NUMBERED_LIST_ITEM: An item in a numbered (ordered) list.
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


class _BaseBlock(BaseNotionModel):
    object: Literal[NotionObjectType.BLOCK] = Field(
        default=NotionObjectType.BLOCK, frozen=True
    )

    id: Optional[NotionObjectId] = Field(default=None)

    parent: Optional[Parent] = Field(default=None)

    created_time: Optional[
        Annotated[str | datetime, BeforeValidator(validate_datetime)]
    ] = Field(default=None, frozen=True)

    last_edited_time: Optional[
        Annotated[str | datetime, BeforeValidator(validate_datetime)]
    ] = Field(default=None, frozen=True)

    created_by: Optional[UserRef] = Field(default=None, frozen=True)

    last_edited_by: Optional[UserRef] = Field(default=None, frozen=True)

    archived: Optional[bool] = Field(default=None, frozen=True)

    in_trash: Optional[bool] = Field(default=None, frozen=True)

    has_children: Optional[bool] = Field(default=None, frozen=True)


class _TextBaseBlockObject(BaseNotionModel):
    """Represents a text-based block value.

    Attributes:
        rich_text: the rich texts in the block.
        color: the color of the block.
        children: the nested child blocks.
    """

    rich_text: list[RichText] = Field(default_factory=list)
    color: Color | BackgroundColor | None = Field(default=None)
    children: Optional[list[Block]] = Field(default_factory=list)


class Bookmark(BaseNotionModel):
    caption: Optional[list[RichText]] = Field(default=None)
    url: Annotated[str, BeforeValidator(validate_url)]


class BulletListItem(_TextBaseBlockObject):
    """Represents a bullet list item.

    Attributes:
        rich_text: the rich texts in the block.
        color: the color of the block.
        children: the nested child blocks.
    """

    pass


class Callout(BaseNotionModel):
    rich_text: list[RichText] = Field(default_factory=list)
    icon: Emojis | File | None = Field(default=None)
    color: Color | BackgroundColor | None = Field(default=None)


class ChildDatabase(BaseNotionModel):
    title: str


class ChildPage(BaseNotionModel):
    title: str


class Code(BaseNotionModel):
    caption: Optional[list[RichText]] = Field(default=None)
    rich_text: list[RichText] = Field(default_factory=list)
    language: ProgrammingLanguage


class CaptionHostedFile(HostedFile):
    caption: Optional[list[RichText]] = Field(default=None)


class CaptionExternalFile(ExternalFile):
    caption: Optional[list[RichText]] = Field(default=None)


CaptionFile = Annotated[
    CaptionHostedFile | CaptionExternalFile, Field(discriminator="type")
]


class CaptionHostedFileWithName(HostedFileWithName):
    caption: Optional[list[RichText]] = Field(default=None)


class CaptionExternalFileWithName(ExternalFileWithName):
    caption: Optional[list[RichText]] = Field(default=None)


CaptionFileWithName = Annotated[
    CaptionHostedFileWithName | CaptionExternalFileWithName, Field(discriminator="type")
]


class Heading(BaseNotionModel):
    rich_text: list[RichText] = Field(default_factory=list)
    color: Color | BackgroundColor | None = Field(default=None)
    is_toggleable: bool = Field(default=False)


class NumberedListItem(_TextBaseBlockObject):
    """Represents a numbered list item.

    Attributes:
        rich_text: the rich texts in the block.
        color: the color of the block.
        children: the nested child blocks.
    """

    pass


class Paragraph(_TextBaseBlockObject):
    """Represents a paragraph block.

    Attributes:
        rich_text: the rich texts in the block.
        color: the color of the block.
        children: the nested child blocks.
    """

    pass


class Quote(_TextBaseBlockObject):
    """Represents a quote block.

    Attributes:
        rich_text: the rich texts in the block.
        color: the color of the block.
        children: the nested child blocks.
    """

    pass


class SyncedFrom(BaseNotionModel):
    """Represents the type of the synced from the object.

    Attributes:
        block_id: The synced block.
    """

    block_id: NotionObjectId


class OriginalSynced(BaseNotionModel):
    synced_form: Literal[None] = Field(default=None, frozen=True)
    children: list[Block] = Field(default_factory=list)


class DuplicateSynced(BaseNotionModel):
    synced_from: SyncedFrom
    children: Literal[None] = Field(default=None, frozen=True)


class Table(BaseNotionModel):
    table_width: Annotated[int, Field(gt=0)]
    has_column_header: bool
    has_row_header: bool


class Cells(BaseNotionModel):
    rich_text: list[RichText] = Field(default_factory=list)


class ToDo(_TextBaseBlockObject):
    """Represents a to-do block.

    Attributes:
        rich_text: the rich texts in the block.
        color: the color of the block.
        children: the nested child blocks.
        checked: the checked status of the to-do block.
    """

    checked: Optional[bool] = Field(default=None)


class Toggle(_TextBaseBlockObject):
    """Represents a toggle block.

    Attributes:
        rich_text: the rich texts in the block.
        color: the color of the block.
        children: the nested child blocks.
    """

    pass


class BookmarkBlock(_BaseBlock):
    type: Literal[BlockType.BOOKMARK] = Field(default=BlockType.BOOKMARK, frozen=True)
    bookmark: Bookmark


class BreadcrumbBlock(_BaseBlock):
    type: Literal[BlockType.BREADCRUMB] = Field(
        default=BlockType.BREADCRUMB, frozen=True
    )
    breadcrumb: dict = Field(default_factory=dict, frozen=True)


class BulletListItemBlock(_BaseBlock):
    type: Literal[BlockType.BULLETED_LIST_ITEM] = Field(
        default=BlockType.BULLETED_LIST_ITEM, frozen=True
    )
    bullet_list_item: BulletListItem


class CalloutBlock(_BaseBlock):
    type: Literal[BlockType.CALLOUT] = Field(default=BlockType.CALLOUT, frozen=True)
    callout: Callout


class ChildDatabaseBlock(_BaseBlock):
    type: Literal[BlockType.CHILD_DATABASE] = Field(
        default=BlockType.CHILD_DATABASE, frozen=True
    )
    child_database: ChildDatabase


class ChildPageBlock(_BaseBlock):
    type: Literal[BlockType.CHILD_PAGE] = Field(
        default=BlockType.CHILD_PAGE, frozen=True
    )
    child_page: ChildPage


class CodeBlock(_BaseBlock):
    type: Literal[BlockType.CODE] = Field(default=BlockType.CODE, frozen=True)
    code: Code


class ColumnListBlock(_BaseBlock):
    type: Literal[BlockType.COLUMN_LIST] = Field(
        default=BlockType.COLUMN_LIST, frozen=True
    )
    column_list: dict = Field(default_factory=dict, frozen=True)


class ColumnBlock(_BaseBlock):
    type: Literal[BlockType.COLUMN] = Field(default=BlockType.COLUMN, frozen=True)
    column: dict = Field(default_factory=dict, frozen=True)


class DividerBlock(_BaseBlock):
    type: Literal[BlockType.DIVIDER] = Field(default=BlockType.DIVIDER, frozen=True)
    divider: dict = Field(default_factory=dict, frozen=True)


class EmbedBlock(_BaseBlock):
    type: Literal[BlockType.EMBED] = Field(default=BlockType.EMBED, frozen=True)
    embed: NotionUrlObject


class EquationBlock(_BaseBlock):
    type: Literal[BlockType.EQUATION] = Field(default=BlockType.EQUATION, frozen=True)
    equation: NotionEquation


class FileBlock(_BaseBlock):
    type: Literal[BlockType.FILE] = Field(default=BlockType.FILE, frozen=True)
    file: CaptionFileWithName


class HeadingOneBlock(_BaseBlock):
    type: Literal[BlockType.HEADING_1] = Field(default=BlockType.HEADING_1, frozen=True)
    heading_1: Heading


class HeadingTwoBlock(_BaseBlock):
    type: Literal[BlockType.HEADING_2] = Field(default=BlockType.HEADING_2, frozen=True)
    heading_2: Heading


class HeadingThreeBlock(_BaseBlock):
    type: Literal[BlockType.HEADING_3] = Field(default=BlockType.HEADING_3, frozen=True)
    heading_3: Heading


class ImageBlock(_BaseBlock):
    type: Literal[BlockType.IMAGE] = Field(default=BlockType.IMAGE, frozen=True)
    image: File


class NumberedListItemBlock(_BaseBlock):
    type: Literal[BlockType.NUMBERED_LIST_ITEM] = Field(
        default=BlockType.NUMBERED_LIST_ITEM, frozen=True
    )
    numbered_list_item: NumberedListItem


class ParagraphBlock(_BaseBlock):
    type: Literal[BlockType.PARAGRAPH] = Field(default=BlockType.PARAGRAPH, frozen=True)
    paragraph: Paragraph


class PdfBlock(_BaseBlock):
    type: Literal[BlockType.PDF] = Field(default=BlockType.PDF, frozen=True)
    pdf: CaptionFile


class QuoteBlock(_BaseBlock):
    type: Literal[BlockType.QUOTE] = Field(default=BlockType.QUOTE, frozen=True)
    quote: Quote


class SyncedBlock(_BaseBlock):
    type: Literal[BlockType.SYNCED_BLOCK] = Field(
        default=BlockType.SYNCED_BLOCK, frozen=True
    )
    synced_block: OriginalSynced | DuplicateSynced


class TableBlock(_BaseBlock):
    type: Literal[BlockType.TABLE] = Field(default=BlockType.TABLE, frozen=True)
    table: Table


class TableRowBlock(_BaseBlock):
    type: Literal[BlockType.TABLE_ROW] = Field(default=BlockType.TABLE_ROW, frozen=True)
    table_row: Cells


class TableContentBlock(_BaseBlock):
    type: Literal[BlockType.TABLE_OF_CONTENTS] = Field(
        default=BlockType.TABLE_OF_CONTENTS, frozen=True
    )
    table_of_contents: Color | BackgroundColor


class ToDoBlock(_BaseBlock):
    type: Literal[BlockType.TO_DO] = Field(default=BlockType.TO_DO, frozen=True)
    to_do: ToDo


class ToggleBlock(_BaseBlock):
    type: Literal[BlockType.TOGGLE] = Field(default=BlockType.TOGGLE, frozen=True)
    toggle: Toggle


class VideoBlock(_BaseBlock):
    type: Literal[BlockType.VIDEO] = Field(default=BlockType.VIDEO, frozen=True)
    video: CaptionFile


class UnsupportedBlock(_BaseBlock):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    type: Literal[BlockType.UNSUPPORTED] = Field(
        default=BlockType.UNSUPPORTED, frozen=True
    )


Block = Annotated[
    BookmarkBlock
    | BreadcrumbBlock
    | BulletListItemBlock
    | CalloutBlock
    | ChildDatabaseBlock
    | ChildPageBlock
    | CodeBlock
    | ColumnBlock
    | ColumnListBlock
    | DividerBlock
    | EmbedBlock
    | EquationBlock
    | FileBlock
    | HeadingOneBlock
    | HeadingTwoBlock
    | HeadingThreeBlock
    | ImageBlock
    | NumberedListItemBlock
    | ParagraphBlock
    | PdfBlock
    | QuoteBlock
    | SyncedBlock
    | TableBlock
    | TableRowBlock
    | TableContentBlock
    | ToDoBlock
    | ToggleBlock
    | VideoBlock
    | UnsupportedBlock,
    Field(discriminator="type"),
]
