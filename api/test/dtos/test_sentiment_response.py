import pytest
from pydantic import ValidationError

from src.dtos import SentimentResponse


class TestSentimentResponseModel:
    """
    Unit tests for SentimentResponse DTO.
    """

    def test_valid_sentiment_response(self):
        sentiment_instance = SentimentResponse(
            feedback="This is a feedback.",
            sentiment="positive",
            response="This is a response.",
            audio="audio_file_path.mp3",
        )
        assert sentiment_instance.feedback == "This is a feedback."
        assert sentiment_instance.sentiment == "positive"
        assert sentiment_instance.response == "This is a response."
        assert sentiment_instance.audio == "audio_file_path.mp3"

    def test_missing_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            SentimentResponse()
        assert "type=missing" in str(exc_info.value)

    def test_invalid_sentiment_type(self):
        with pytest.raises(ValidationError) as exc_info:
            SentimentResponse(
                sentiment=123, response="Valid response", audio="audio.mp3"
            )
        assert "type=string_type" in str(exc_info.value)

    def test_invalid_response_type(self):
        with pytest.raises(ValidationError) as exc_info:
            SentimentResponse(sentiment="negative", response=456, audio="audio.mp3")
        assert "type=string_type" in str(exc_info.value)

    def test_invalid_audio_type(self):
        with pytest.raises(ValidationError) as exc_info:
            SentimentResponse(
                sentiment="neutral", response="Another response", audio=789
            )
        assert "type=string_type" in str(exc_info.value)
