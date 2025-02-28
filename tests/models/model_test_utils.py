import pytest
from pydantic import BaseModel


class PydanticModelTester:

    def __init__(self, model_class: type, test_data: list[tuple[BaseModel, dict, ...]]):
        """
        Initialize the tester with model class and test data.

        Args:
            model_class: Pydantic model class to test
            test_data: List of valid data dictionaries
        """
        self.model_class = model_class
        self.test_data = test_data

    def _test_valid_serialization(self):
        """
        Test serialization of valid data instances.
        Checks model creation, attribute matching, and dictionary conversion.
        """
        # Test valid data serialization
        for test_model, test_dict in self.test_data:
            try:
                model = self.model_class(**test_dict)
                # Verify model
                assert test_model == model

                # Verify JSON serialization
                json_data = model.model_dump_json()
                reconstructed_model = self.model_class.model_validate_json(json_data)
                assert test_model == reconstructed_model
            except Exception as e:
                pytest.fail(f"Failed to serialize valid data {test_dict}: {e}")

    def run_all_tests(self):
        """
        Run both serialization tests.
        Can be used directly in test files or as a standalone test method.
        """
        self._test_valid_serialization()
