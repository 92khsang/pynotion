from datetime import timezone

import pytest
from pydantic import ValidationError

from pynotion.models.file import *
from tests.models.model_test_utils import (
    PydanticModelTester,
    DiscriminatedModelTester,
)


@pytest.mark.parametrize(
    "clz, values, should_raise",
    [
        (ExternalFileObject, {"url": "https://valid-url.com/"}, False),
        (
            HostedFileObject,
            {
                "url": "https://valid-url.com/file.png",
                "expiry_time": "2024-05-17T15:30:00Z",
            },
            False,
        ),
        (
            HostedFileObject,
            {
                "url": "https://valid-url.com/file.png",
                "expiry_time": datetime(2024, 5, 17, 15, 30, tzinfo=timezone.utc),
            },
            False,
        ),
        (
            HostedFileObject,
            {"url": "invalid-url", "expiry_time": "2024-05-17T15:30:00Z"},
            True,
        ),  # Invalid URL
        (
            HostedFileObject,
            {
                "url": "https://valid-url.com/file.png",
                "expiry_time": "invalid-datetime",
            },
            True,
        ),  # Invalid datetime
    ],
)
def test_notion_hosted_file(clz, values, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            clz(**values)
    else:
        notion_file = clz(**values)
        assert notion_file.url == values["url"]
        if clz is HostedFileObject:
            expiry_time = values.get("expiry_time", None)
            assert (
                notion_file.expiry_time == expiry_time
                if isinstance(expiry_time, datetime)
                else datetime.fromisoformat(expiry_time)
            )


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            File,
            HostedFile,
            {
                "type": FileType.FILE,
                "file": HostedFileObject(
                    url="https://valid-url.com", expiry_time="2024-05-17T15:30:00Z"
                ),
            },
        ),
        (
            File,
            ExternalFile,
            {
                "type": FileType.EXTERNAL,
                "external": ExternalFileObject(url="https://external.com"),
            },
        ),
    ],
)
def test_discriminated_model(annotated_clz: type, expected_clz: type, input_data: dict):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "model_class, test_data",
    [
        (
            HostedFile,
            (
                {
                    "type": FileType.FILE,
                    "file": {
                        "url": "https://notion.so",
                        "expiry_time": "2024-05-17T15:30:00Z",
                    },
                },
                {
                    "type": FileType.FILE,
                    "file": {
                        "url": "https://notion.so",
                        "expiry_time": datetime(
                            2024, 5, 17, 15, 30, tzinfo=timezone.utc
                        ),
                    },
                },
                {
                    "type": FileType.FILE.value,
                    "file": {
                        "url": "https://notion.so",
                        "expiry_time": "2024-05-17T15:30:00Z",
                    },
                },
            ),
        ),
        (
            ExternalFile,
            (
                {
                    "type": FileType.EXTERNAL,
                    "external": {"url": "https://example.com"},
                },
                {
                    "type": FileType.EXTERNAL,
                    "external": {"url": "https://example.com"},
                },
                {
                    "type": FileType.EXTERNAL.value,
                    "external": {"url": "https://example.com"},
                },
            ),
        ),
    ],
)
def test_pydantic_models(model_class, test_data):
    tester = PydanticModelTester(model_class, test_data)
    tester.run_all_tests()
