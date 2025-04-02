from enum import Enum
from typing import Literal, Annotated, TYPE_CHECKING, Union

from pydantic import Field, BeforeValidator

from ._internal import (
    BaseNotionModel,
    validate_url,
)
from ._internal.utils import discriminate_field

if TYPE_CHECKING:
    from .types import NotionDatetime

__all__ = [
    "FileType",
    "HostedFileObject",
    "ExternalFileObject",
    "HostedFile",
    "HostedFileWithName",
    "ExternalFile",
    "ExternalFileWithName",
    "NotionFile",
    "NotionFileWithName",
    "FILE_CLASS_MAP",
    "File_WITH_NAME_CLASS_MAP",
]


class FileType(str, Enum):
    """Defines the possible file types in Notion.

    Attributes:
        FILE: File hosted by Notion with an expiry time.
        EXTERNAL: File hosted externally (linked by URL).
    """

    FILE = "file"
    EXTERNAL = "external"


class HostedFileObject(BaseNotionModel):
    """Represents a file hosted by Notion.

    Notion-hosted files have a URL that expires after a period of time.

    Attributes:
        url: The URL of the hosted file.
        expiry_time: The ISO 8601 datetime when the URL will expire.
    """

    url: Annotated[str, BeforeValidator(validate_url)]
    expiry_time: "NotionDatetime"


class ExternalFileObject(BaseNotionModel):
    """Represents an externally hosted file in Notion.

    Attributes:
        url: The URL of the externally hosted file.
    """

    url: Annotated[str, BeforeValidator(validate_url)]


class HostedFile(BaseNotionModel):
    """Represents a file hosted by Notion.

    Attributes:
        type: The type of the file.
        file: The hosted file object.
    """

    type: Literal[FileType.FILE] = Field(default=FileType.FILE, frozen=True)
    file: "HostedFileObject"


class ExternalFile(BaseNotionModel):
    """Represents an externally hosted file in Notion.

    Attributes:
        type: The type of the file.
        external: The URL of the externally hosted file.
    """

    type: Literal[FileType.EXTERNAL] = Field(default=FileType.EXTERNAL, frozen=True)
    external: "ExternalFileObject"


class HostedFileWithName(BaseNotionModel):
    """Represents a file hosted by Notion.

    Attributes:
        type: The type of the file.
        file: The hosted file object.
    """

    type: Literal[FileType.FILE] = Field(default=FileType.FILE, frozen=True)
    file: "HostedFileObject"
    name: str


class ExternalFileWithName(BaseNotionModel):
    """Represents an externally hosted file in Notion.

    Attributes:
        type: The type of the file.
        external: The URL of the externally hosted file.
        name: The name of the file.
    """

    type: Literal[FileType.EXTERNAL] = Field(default=FileType.EXTERNAL, frozen=True)
    external: "ExternalFileObject"
    name: str


FILE_CLASS_MAP = {
    FileType.FILE: "HostedFile",
    FileType.EXTERNAL: "ExternalFile",
}


NotionFile = Annotated[
    Union[tuple(FILE_CLASS_MAP.values())],
    BeforeValidator(lambda v: discriminate_field(v, "type", FILE_CLASS_MAP)),
]

File_WITH_NAME_CLASS_MAP = {
    FileType.FILE: "HostedFileWithName",
    FileType.EXTERNAL: "ExternalFileWithName",
}


NotionFileWithName = Annotated[
    Union[tuple(File_WITH_NAME_CLASS_MAP.values())],
    BeforeValidator(lambda v: discriminate_field(v, "type", File_WITH_NAME_CLASS_MAP)),
]
