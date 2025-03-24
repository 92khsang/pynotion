from __future__ import annotations as _annotations

from enum import Enum
from typing import Literal, Annotated

from pydantic import Field, BeforeValidator

from ._internal import (
    BaseNotionModel,
    validate_url,
)
from .types import NotionDatetime


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
    expiry_time: NotionDatetime


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
    file: HostedFileObject


class HostedFileWithName(HostedFile):
    """Represents a file hosted by Notion with a name.

    Attributes:
        type: The type of the file.
        file: The hosted file object.
        name: The name of the file.
    """

    name: str


class ExternalFile(BaseNotionModel):
    """Represents an externally hosted file in Notion.

    Attributes:
        type: The type of the file.
        external: The URL of the externally hosted file.
    """

    type: Literal[FileType.EXTERNAL] = Field(default=FileType.EXTERNAL, frozen=True)
    external: ExternalFileObject


class ExternalFileWithName(ExternalFile):
    """Represents an externally hosted file in Notion with a name.

    Attributes:
        type: The type of the file.
        external: The URL of the externally hosted file.
        name: The name of the file.
    """

    name: str


File = Annotated[HostedFile | ExternalFile, Field(discriminator="type")]
FileWithName = Annotated[
    HostedFileWithName | ExternalFileWithName, Field(discriminator="type")
]
