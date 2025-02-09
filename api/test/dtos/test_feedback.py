import pytest
from pydantic import ValidationError
from src.dtos import Feedback


class TestFeedbackModel:
    """
    Unit tests for Feedback DTO.
    """

    def test_valid_feedback(self):
        feedback_instance = Feedback(feedback="This is a valid feedback message.")
        assert feedback_instance.feedback == "This is a valid feedback message."

    def test_missing_feedback(self):
        with pytest.raises(ValidationError) as exc_info:
            Feedback()
        assert "type=missing" in str(exc_info.value)

    def test_invalid_feedback_type(self):
        with pytest.raises(ValidationError) as exc_info:
            Feedback(feedback=123)
        assert "type=string_type" in str(exc_info.value)
