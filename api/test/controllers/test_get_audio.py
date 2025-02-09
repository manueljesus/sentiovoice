import pytest
from typing import Generator
from unittest.mock import MagicMock, patch

from fastapi import status
from fastapi.testclient import TestClient

from src.api import api


class TestDownloadAudio:
    """
    GET /audio/{filename} endpoint test.
    """

    @pytest.fixture
    def client(self) -> TestClient:
        """
        FastAPI test client.
        """
        return TestClient(app=api)

    @pytest.fixture
    def mock_file_exists(self) -> Generator[MagicMock, None, None]:
        """
        Patch os.path.isfile to simulate file existence.
        """
        with patch("os.path.isfile", return_value=True) as mock:
            yield mock

    @pytest.fixture
    def mock_file_response(self) -> Generator[MagicMock, None, None]:
        """
        Patch FileResponse to avoid real file access.
        """
        with patch("src.controllers.get_audio.FileResponse") as mock:
            mock.return_value = MagicMock()
            yield mock

    def test_download_audio_success(
        self, client: TestClient, mock_file_exists, mock_file_response
    ):
        filename = "test.mp3"
        response = client.get(f"/audio/{filename}")
        path = f"test_audio_path/{filename}"

        assert response.status_code == status.HTTP_200_OK
        mock_file_exists.assert_called_once_with(path)
        mock_file_response.assert_called_once_with(
            path=path, media_type="audio/mpeg", filename=filename
        )

    def test_download_audio_file_not_found(self, client: TestClient):
        with patch("os.path.isfile", return_value=False):
            filename = "nonexistent.mp3"
            response = client.get(f"/audio/{filename}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "File not found"

    def test_download_audio_invalid_filename(self, client: TestClient):
        filename = "invalid.txt"
        response = client.get(f"/audio/{filename}")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Invalid filename"
