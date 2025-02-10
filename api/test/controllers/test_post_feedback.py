import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.api import api


class TestFeedbackEndpoint:
    @pytest.fixture
    def client(self) -> TestClient:
        """
        FastAPI TestClient.
        """
        return TestClient(app=api)

    @pytest.fixture
    def mock_text_analytics(self):
        """
        Patch azure_text_analytics_client.analyze_sentiment to return 'positive'.
        """
        with patch("src.actions.generate_feedback_response.azure_text_analytics_client.analyze_sentiment") as mock:
            mock.return_value = "positive"
            yield mock

    @pytest.fixture
    def mock_openai_client(self):
        """
        Patch azure_openai_client to return a simple string response.
        """
        with patch("src.actions.generate_feedback_response.azure_openai_client") as mock:
            mock.return_value = "Thank you!"
            yield mock

    @pytest.fixture
    def mock_speech_synthesis_client(self):
        """
        Patch azure_speech_synthesis_client to return an audio file path.
        """
        with patch("src.actions.generate_feedback_response.azure_speech_synthesis_client") as mock:
            mock.return_value = "audio.mp3"
            yield mock

    @pytest.fixture
    def mock_prompt(self):
        """
        Patch Prompt so that Prompt() returns a mock instance that returns 'Generated prompt'.
        """
        with patch("src.actions.generate_feedback_response.Prompt") as mock_class:
            prompt_instance = MagicMock()
            prompt_instance.return_value = "Generated prompt"
            mock_class.return_value = prompt_instance
            yield mock_class

    def test_process_feedback_endpoint(
        self,
        client: TestClient,
        mock_text_analytics,
        mock_openai_client,
        mock_speech_synthesis_client,
        mock_prompt,
    ):
        payload = {"feedback": "I love SentioVoice!"}
        response = client.post("/feedback/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data == {
            "feedback": "I love SentioVoice!",
            "response": "Thank you!",
            "sentiment": "positive",
            "audio": "audio.mp3"
        }

        mock_text_analytics.assert_called_once_with("I love SentioVoice!")
        mock_prompt.assert_called_once()
        mock_prompt.return_value.assert_called_once_with("positive", "I love SentioVoice!")
        mock_openai_client.assert_called_once_with("Generated prompt")
        mock_speech_synthesis_client.assert_called_once_with("Thank you!", "positive")
