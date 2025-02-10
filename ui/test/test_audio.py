import pytest
import os
from typing import Generator
from unittest.mock import patch, MagicMock

from src.audio import Audio


class TestAudio:
    """Test suite for the Audio module."""
    @pytest.fixture
    def mock_get(self) -> Generator[MagicMock, None, None]:
        with patch("requests.get") as mock:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = b"audio_data"
            mock.return_value = mock_response
            yield mock

    @pytest.fixture
    def mock_os_exists(self) -> Generator[MagicMock, None, None]:
        with patch("os.path.exists", return_value=True) as mock:
            yield mock

    @pytest.fixture
    def mock_os_listdir(self) -> Generator[MagicMock, None, None]:
        with patch("os.listdir", return_value=["test_audio.mp3"]) as mock:
            yield mock

    @pytest.fixture
    def mock_os_remove(self) -> Generator[MagicMock, None, None]:
        with patch("os.remove") as mock:
            yield mock

    @pytest.fixture
    def mock_os_makedirs(self) -> Generator[MagicMock, None, None]:
        with patch("os.makedirs") as mock:
            yield mock

    @pytest.fixture
    def mock_streamlit_error(self) -> Generator[MagicMock, None, None]:
        with patch("streamlit.error") as mock:
            yield mock

    @pytest.fixture
    def mock_streamlit_audio(self) -> Generator[MagicMock, None, None]:
        with patch("streamlit.audio") as mock:
            yield mock

    @pytest.fixture
    def audio(self) -> Audio:
        return Audio()

    def test_clear(
        self,
        mock_os_exists: MagicMock,
        mock_os_listdir: MagicMock,
        mock_os_remove: MagicMock,
        mock_os_makedirs: MagicMock,
        audio: Audio
    ):
        """Test that clear method correctly removes files and creates the audio directory."""
        audio.clear()
        mock_os_remove.assert_called_once_with(os.path.join(audio.audio_dir, "test_audio.mp3"))

    def test_download_success(
        self,
        mock_get: MagicMock,
        audio: Audio
    ):
        """Test that download method correctly saves the audio file."""
        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            file_path = audio.download("test_audio.mp3")
            mock_open.assert_called_once_with(os.path.join(audio.audio_dir, "test_audio.mp3"), "wb")
            assert file_path == os.path.join(audio.audio_dir, "test_audio.mp3")

    def test_download_failure(
        self,
        mock_get: MagicMock,
        mock_streamlit_error: MagicMock,
        audio: Audio
    ):
        """Test that download method handles API failure properly."""
        mock_get.return_value.status_code = 500
        file_path = audio.download("test_audio.mp3")
        mock_streamlit_error.assert_called_once_with("Failed to download the audio file.")
        assert file_path is None

    def test_play_success(
        self,
        mock_os_exists: MagicMock,
        mock_streamlit_audio: MagicMock,
        audio: Audio
    ):
        """Test that play plays an existing file."""
        with patch("builtins.open", new_callable=MagicMock) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = b"audio_data"
            audio.play("test_audio.mp3")
            mock_streamlit_audio.assert_called_once_with(b"audio_data", format="audio/mpeg")

    def test_play_failure(
        self,
        mock_streamlit_error: MagicMock,
        audio: Audio
    ):
        """Test that play handles missing file properly."""
        with patch("os.path.exists", return_value=False):
            audio.play("test_audio.mp3")
            mock_streamlit_error.assert_called_once_with("Audio file not found.")
