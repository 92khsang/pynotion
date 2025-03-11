import json
from typing import Any, TypeAlias

import pytest
from pydantic import BaseModel, TypeAdapter

# Type aliases for better readability
Diffdict: TypeAlias = dict[str, Any]
Mismatchdict: TypeAlias = dict[str, tuple[Any, Any]]
FormattedResult: TypeAlias = str


def _format_dict(d: dict[str, Any], level: int = 1) -> str:
    """
    Format a dictionary with proper indentation.

    Args:
        d: dictionary to format
        level: Current indentation level

    Returns:
        Formatted string representation of the dictionary
    """
    if not d:
        return "{}"

    indent = "    " * level
    prev_level_indent = "    " * (level - 1)

    entries = [
        f"{indent}{repr(k)}: {_format_value(v, level + 1)}," for k, v in d.items()
    ]

    return "{\n" + "\n".join(entries) + f"\n{prev_level_indent}}}"


def _format_value(val: Any, level: int = 1) -> str:
    """
    Format a value, with special handling for dictionaries.

    Args:
        val: Value to format
        level: Current indentation level

    Returns:
        Formatted string representation of the value
    """
    if isinstance(val, dict):
        return _format_dict(val, level)
    return repr(val)


def _format_mismatch(m: Mismatchdict, level: int = 1) -> str:
    """
    Format mismatch dictionary showing expected vs actual values.

    Args:
        m: dictionary of mismatches
        level: Current indentation level

    Returns:
        Formatted string representation of mismatches
    """
    if not m:
        return "{}"

    indent = "    " * level
    prev_level_indent = "    " * (level - 1)

    entries = []
    for k, (expected_val, actual_val) in m.items():
        entries.append(
            f"{indent}{repr(k)}:\n"
            f"{indent}    Expected: {_format_value(expected_val, level + 1)},\n"
            f"{indent}    Actual: {_format_value(actual_val, level + 1)},"
        )

    return "{\n" + "\n".join(entries) + f"\n{prev_level_indent}}}"


def find_mismatch(expected: dict[str, Any], actual: dict[str, Any]) -> FormattedResult:
    """
    Compare two dictionaries and identify differences between them.

    Args:
        expected: dictionary containing expected values
        actual: dictionary containing actual values

    Returns:
        A formatted string showing differences categorized as:
        - Keys only in expected
        - Keys only in actual
        - Keys in both but with different values
    """
    expected_only: Diffdict = {k: v for k, v in expected.items() if k not in actual}
    actual_only: Diffdict = {k: v for k, v in actual.items() if k not in expected}
    mismatch: Mismatchdict = {
        k: (expected[k], actual[k])
        for k in set(expected) & set(actual)
        if expected[k] != actual[k]
    }

    return (
        f"\n    Expected Only: {_format_dict(expected_only)}"
        f"\n    Actual Only: {_format_dict(actual_only)}"
        f"\n    Mismatch: {_format_mismatch(mismatch)}"
    )


class PydanticModelTester:
    """
    A utility class to test serialization and validation of Pydantic models.

    This class ensures that:
    - The model can be instantiated correctly with valid input data.
    - The dictionary representation matches expected values.
    - JSON serialization works as expected.
    """

    def __init__(
        self,
        model_class: type[BaseModel],
        test_data: tuple[dict, dict, dict],
    ):
        """
        Initialize the tester with a Pydantic model class and test data.

        Args:
            model_class (type[BaseModel]): The Pydantic model class to test.
            test_data (tuple[dict, dict, dict]): A tuple containing:
                - input_dict (dict): The input data for model instantiation.
                - expected_dict (dict): The expected dictionary output.
                - expected_json (dict): The expected JSON-serializable output.
        """
        self.model_class = model_class
        self.input_dict, self.expected_dict, self.expected_json = test_data
        self.model_instance = None  # Will store the model instance after creation

    def _instantiate_model(self):
        """Instantiate the Pydantic model with input data."""
        try:
            self.model_instance = self.model_class(**self.input_dict)
        except Exception as e:
            pytest.fail(f"Model instantiation failed: {e}")

    def _validate_dict_serialization(self):
        """Validate dictionary serialization using TypeAdapter."""
        try:
            model_dict = TypeAdapter(self.model_class).dump_python(
                self.model_instance, exclude_none=True
            )
            assert (
                model_dict == self.expected_dict
            ), f"dictionary mismatch: {find_mismatch(self.expected_dict, model_dict)}"
        except AssertionError as e:
            pytest.fail(f"dictionary validation failed: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during dictionary serialization: {e}")

    def _validate_model_dump(self):
        """Validate dictionary conversion using model_dump()."""
        try:
            model_dump_dict = self.model_instance.model_dump(
                by_alias=True, exclude_none=True
            )
            assert (
                model_dump_dict == self.expected_dict
            ), f"model_dump() output mismatch: {find_mismatch(self.expected_dict, model_dump_dict)}"
        except AssertionError as e:
            pytest.fail(f"model_dump validation failed: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during model_dump serialization: {e}")

    def _validate_json_serialization(self):
        """Validate JSON serialization of the model."""
        try:
            json_data = TypeAdapter(self.model_class).dump_json(
                self.model_instance, exclude_none=True, exclude_defaults=True
            )
            assert (
                json.loads(json_data) == self.expected_json
            ), f"JSON mismatch: {find_mismatch(self.expected_json, json.loads(json_data))}"
        except AssertionError as e:
            pytest.fail(f"JSON validation failed: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error during JSON serialization: {e}")

    def run_all_tests(self):
        """Run all serialization and validation tests."""
        self._instantiate_model()
        if self.model_instance:
            self._validate_dict_serialization()
            self._validate_model_dump()
            self._validate_json_serialization()
