from uuid import uuid4

import pytest
from pydantic import ValidationError

from pynotion.models.emoji import *
from tests.models.model_test_utils import (
    PydanticModelTester,
    DiscriminatedModelTester,
)


@pytest.mark.parametrize(
    "clz, emoji_type, type_object, should_raise",
    [
        (Emoji, EmojiType.EMOJI, "🔥", False),
        (
            CustomEmoji,
            EmojiType.CUSTOM_EMOJI,
            CustomEmojiObject(id=uuid4(), name="custom", url="https://valid-url.com"),
            False,
        ),
        (
            CustomEmoji,
            EmojiType.EMOJI,
            CustomEmojiObject(id=uuid4(), name="custom", url="https://valid-url.com"),
            True,
        ),  # Invalid type_object
        (Emoji, EmojiType.CUSTOM_EMOJI, "🔥", True),  # Invalid type_object
    ],
)
def test_notion_emoji(clz, emoji_type, type_object, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            clz(type=emoji_type, **{emoji_type.value: type_object})
    else:
        notion_emoji = clz(type=emoji_type, **{emoji_type.value: type_object})
        assert notion_emoji.type == emoji_type
        assert getattr(notion_emoji, emoji_type.value) == type_object


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            Emojis,
            Emoji,
            {
                "type": EmojiType.EMOJI,
                "emoji": "🔥",
            },
        ),
        (
            Emojis,
            CustomEmoji,
            {
                "type": EmojiType.CUSTOM_EMOJI,
                "custom_emoji": CustomEmojiObject(
                    id=uuid4(), name="custom_emoji", url="https://valid-url.com"
                ),
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
            Emoji,
            (
                {"type": "emoji", "emoji": "🔥"},
                {"type": EmojiType.EMOJI, "emoji": "🔥"},
                {"type": "emoji", "emoji": "🔥"},
            ),
        ),
        (
            CustomEmoji,
            (
                {
                    "type": "custom_emoji",
                    "custom_emoji": {
                        "id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                        "name": "smile",
                        "url": "https://example.com/emoji.png",
                    },
                },
                {
                    "type": EmojiType.CUSTOM_EMOJI,
                    "custom_emoji": {
                        "id": UUID("f4de14e1-0cff-4497-835f-29d6d04d62c1"),
                        "name": "smile",
                        "url": "https://example.com/emoji.png",
                    },
                },
                {
                    "type": "custom_emoji",
                    "custom_emoji": {
                        "id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                        "name": "smile",
                        "url": "https://example.com/emoji.png",
                    },
                },
            ),
        ),
    ],
)
def test_pydantic_models(model_class, test_data):
    tester = PydanticModelTester(model_class, test_data)
    tester.run_all_tests()
