import pytest
from typing import Generator
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.api import api


class TestHealthCheck:
    """
    GET /health endpoint test.
    """

    @pytest.fixture
    def client(self) -> TestClient:
        """
        FastAPI test client.
        """
        return TestClient(app=api)

    @pytest.fixture
    def mock_check_azure_openai_client(self) -> Generator[MagicMock, None, None]:
        with patch("src.controllers.get_health._check_azure_openai_client") as mock:
            yield mock

    @pytest.fixture
    def mock_check_azure_text_analytics_client(self) -> Generator[MagicMock, None, None]:
        """Mock Azure Text Analytics client check."""
        with patch("src.controllers.get_health._check_azure_text_analytics_client") as mock:
            yield mock

    @pytest.fixture
    def mock_check_azure_speech_synthesis_client(self) -> Generator[MagicMock, None, None]:
        """Mock Azure Speech Synthesis client check."""
        with patch("src.controllers.get_health._check_azure_speech_synthesis_client") as mock:
            yield mock

    def test_health_check_all_services_available(
        self,
        client: TestClient,
        mock_check_azure_openai_client: MagicMock,
        mock_check_azure_text_analytics_client: MagicMock,
        mock_check_azure_speech_synthesis_client: MagicMock
    ):
        """Test health check when all services are available."""
        mock_check_azure_openai_client.return_value = True
        mock_check_azure_text_analytics_client.return_value = True
        mock_check_azure_speech_synthesis_client.return_value = True

        response = client.get("/health/")
        assert response.status_code == 200
        assert response.json() == {
            "azure_open_ai_client": True,
            "azure_text_analytics_client": True,
            "azure_speech_synthesis_client": True,
        }

    def test_health_check_some_services_unavailable(
        self,
        client: TestClient,
        mock_check_azure_openai_client: MagicMock,
        mock_check_azure_text_analytics_client: MagicMock,
        mock_check_azure_speech_synthesis_client: MagicMock
    ):
        """Test health check when one or more services are unavailable."""
        mock_check_azure_openai_client.return_value = False
        mock_check_azure_text_analytics_client.return_value = True
        mock_check_azure_speech_synthesis_client.return_value = True

        response = client.get("/health/")
        assert response.status_code == 500
        assert response.json()["detail"]["message"] == "One or more Azure services are unavailable"
        assert response.json()["detail"]["status"] == {
            "azure_open_ai_client": False,
            "azure_text_analytics_client": True,
            "azure_speech_synthesis_client": True,
        }

    def test_health_check_all_services_unavailable(
        self,
        client: TestClient,
        mock_check_azure_openai_client: MagicMock,
        mock_check_azure_text_analytics_client: MagicMock,
        mock_check_azure_speech_synthesis_client: MagicMock
    ):
        """Test health check when all services are unavailable."""
        mock_check_azure_openai_client.return_value = False
        mock_check_azure_text_analytics_client.return_value = False
        mock_check_azure_speech_synthesis_client.return_value = False

        response = client.get("/health/")
        assert response.status_code == 500
        assert response.json()["detail"]["message"] == "One or more Azure services are unavailable"
        assert response.json()["detail"]["status"] == {
            "azure_open_ai_client": False,
            "azure_text_analytics_client": False,
            "azure_speech_synthesis_client": False,
        }
