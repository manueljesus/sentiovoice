import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from src.actions.generate_feedback_response import GenerateFeedbackResponse
from src.dtos import Feedback, SentimentResponse


class TestGenerateFeedbackResponse:
    """
    Tests for the GenerateFeedbackResponse workflow.
    """

    @pytest.fixture
    def feedback(self):
        return Feedback(feedback="This is a test feedback.")

    @pytest.fixture
    def mock_text_analytics(self) -> Generator[MagicMock, None, None]:
        with patch("src.actions.generate_feedback_response.azure_text_analytics_client.analyze_sentiment") as mock:
            mock.return_value = "positive"
            yield mock

    @pytest.fixture
    def mock_prompt(self) -> Generator[MagicMock, None, None]:
        """
        Patch the Prompt class so that calling Prompt()(sentiment, feedback) returns "Generated prompt".
        """
        with patch("src.actions.generate_feedback_response.Prompt") as mock_prompt_class:
            prompt_instance = MagicMock()
            prompt_instance.return_value = "Generated prompt"
            mock_prompt_class.return_value = prompt_instance

            yield mock_prompt_class

    @pytest.fixture
    def mock_openai_client(self) -> Generator[MagicMock, None, None]:
        with patch("src.actions.generate_feedback_response.azure_openai_client") as mock:
            mock.return_value = "Generated response"
            yield mock

    @pytest.fixture
    def mock_speech_synthesis_client(self) -> Generator[MagicMock, None, None]:
        with patch("src.actions.generate_feedback_response.azure_speech_synthesis_client") as mock:
            mock.return_value = "audio.mp3"
            yield mock

    @pytest.fixture
    def generate_feedback_response(self) -> GenerateFeedbackResponse:
        return GenerateFeedbackResponse()

    def test_generate_feedback_response(
        self,
        feedback: Feedback,
        mock_text_analytics: MagicMock,
        mock_prompt: MagicMock,
        mock_openai_client: MagicMock,
        mock_speech_synthesis_client: MagicMock,
        generate_feedback_response: GenerateFeedbackResponse,
    ):
        response = generate_feedback_response(feedback)

        mock_text_analytics.assert_called_once_with(feedback.feedback)
        mock_prompt.assert_called_once()
        mock_prompt.return_value.assert_called_once_with("positive", feedback.feedback)
        mock_openai_client.assert_called_once_with("Generated prompt")
        mock_speech_synthesis_client.assert_called_once_with("Generated response", "positive")

        assert isinstance(response, SentimentResponse)
        assert response.feedback == feedback.feedback
        assert response.response == "Generated response"
        assert response.sentiment == "positive"
        assert response.audio == "audio.mp3"
