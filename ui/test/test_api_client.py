import pytest
from typing import Generator
from unittest.mock import patch, MagicMock

from src.api_client import APIClient
from src.settings import settings


class TestAPIClient:
    """Test suite for the API Client"""
    @pytest.fixture
    def mock_get_audio(self) -> Generator[MagicMock, None, None]:
        with patch("requests.get") as mock:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = b"audio_data"
            mock.return_value = mock_response
            yield mock

    @pytest.fixture
    def mock_post_feedback(self) -> Generator[MagicMock, None, None]:
        with patch("requests.post") as mock:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "feedback": "Great app!",
                "sentiment": "positive",
                "response": "Thank you!",
                "audio": "response_audio.mp3"
            }
            mock.return_value = mock_response
            yield mock

    @pytest.fixture
    def client(self) -> APIClient:
        return APIClient()

    def test_get_audio(
        self,
        mock_get_audio: MagicMock,
        client: APIClient
    ):
        """Test if get_audio correctly requests the audio file."""
        response = client.get_audio("test_audio.mp3")

        mock_get_audio.assert_called_once_with(f"{settings.api_url}/audio/test_audio.mp3")
        assert response.status_code == 200
        assert response.content == b"audio_data"

    def test_post_feedback(
        self,
        mock_post_feedback: MagicMock,
        client: APIClient
    ):
        """Test if post_feedback correctly sends feedback to the API."""
        feedback = "Great app!"
        response = client.post_feedback(feedback)

        mock_post_feedback.assert_called_once_with(
            f"{settings.api_url}/feedback", json={"feedback": feedback}
        )
        assert response.status_code == 200
        assert response.json()["feedback"] == "Great app!"
        assert response.json()["sentiment"] == "positive"
        assert response.json()["response"] == "Thank you!"
        assert response.json()["audio"] == "response_audio.mp3"
