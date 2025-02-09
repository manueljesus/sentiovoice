import pytest
from typing import Generator

from unittest.mock import patch, MagicMock

from src.feedback import Feedback
from src.audio import Audio


class TestFeedback:
    """ Test suite for the Feedback module. """
    @pytest.fixture
    def mock_api_post_feedback(self) -> Generator[MagicMock, None, None]:
        with patch("src.api_client.APIClient.post_feedback") as mock_post_feedback:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "sentiment": "POSITIVE",
                "response": "Thank you for your feedback!",
                "audio": "feedback_audio.mp3"
            }
            mock_post_feedback.return_value = mock_response
            yield mock_post_feedback

    @pytest.fixture
    def mock_audio_clear(self) -> Generator[MagicMock, None, None]:
        with patch.object(Audio, "clear") as mock_clear:
            yield mock_clear

    @pytest.fixture
    def mock_audio_download(self) -> Generator[MagicMock, None, None]:
        with patch.object(Audio, "download", return_value="/path/to/audio.mp3") as mock_download:
            yield mock_download

    @pytest.fixture
    def mock_audio_play(self) -> Generator[MagicMock, None, None]:
        with patch.object(Audio, "play") as mock_play:
            yield mock_play

    @pytest.fixture
    def mock_streamlit_write(self) -> Generator[MagicMock, None, None]:
        with patch("streamlit.write") as mock_write:
            yield mock_write

    @pytest.fixture
    def mock_streamlit_error(self) -> Generator[MagicMock, None, None]:
        with patch("streamlit.error") as mock_error:
            yield mock_error

    @pytest.fixture
    def mock_streamlit_warning(self) -> Generator[MagicMock, None, None]:
        with patch("streamlit.warning") as mock_warning:
            yield mock_warning

    @pytest.fixture
    def mock_streamlit_info(self) -> Generator[MagicMock, None, None]:
        with patch("streamlit.info") as mock_info:
            yield mock_info

    @pytest.fixture
    def mock_streamlit_markdown(self) -> Generator[MagicMock, None, None]:
        with patch("streamlit.markdown") as mock_markdown:
            yield mock_markdown

    @pytest.fixture
    def feedback(self) -> Feedback:
        return Feedback()

    def test_process_feedback_success(
        self,
        mock_api_post_feedback: MagicMock,
        mock_audio_clear: MagicMock,
        mock_audio_download: MagicMock,
        mock_audio_play: MagicMock,
        mock_streamlit_write: MagicMock,
        mock_streamlit_markdown: MagicMock,
        feedback: Feedback
    ):
        feedback.process_feedback("Great job!")

        mock_api_post_feedback.assert_called_once_with("Great job!")
        mock_audio_clear.assert_called_once()
        mock_audio_download.assert_called_once_with("feedback_audio.mp3")
        mock_audio_play.assert_called_once_with("feedback_audio.mp3")
        mock_streamlit_write.assert_called_with("Thank you for your feedback!")
        mock_streamlit_markdown.assert_called()

    def test_process_feedback_api_error(
        self,
        mock_api_post_feedback: MagicMock,
        mock_streamlit_error: MagicMock,
        feedback: Feedback
    ):
        mock_api_post_feedback.side_effect = Exception("API Error")
        feedback.process_feedback("Great job!")
        mock_streamlit_error.assert_called_once_with("Error processing feedback. Please try again.")

    def test_process_feedback_no_audio(
        self,
        mock_api_post_feedback: MagicMock,
        mock_audio_download: MagicMock,
        mock_streamlit_write: MagicMock,
        mock_streamlit_info: MagicMock,
        mock_streamlit_warning: MagicMock,
        feedback: Feedback
    ):
        mock_api_post_feedback.return_value.json.return_value["audio"] = ""
        feedback.process_feedback("Great job!")

        mock_streamlit_write.assert_called_with("Thank you for your feedback!")
        mock_streamlit_info.assert_called_once_with("No audio file returned by the API.")
        mock_streamlit_warning.assert_not_called()
