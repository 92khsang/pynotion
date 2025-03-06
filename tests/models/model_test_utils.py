import json

import pytest
from pydantic import BaseModel, TypeAdapter


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
            ), f"dictionary mismatch: {model_dict} != {self.expected_dict}"
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
            ), f"model_dump() output mismatch: {model_dump_dict} != {self.expected_dict}"
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
            ), f"JSON mismatch: {json.loads(json_data)} != {self.expected_json}"
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
