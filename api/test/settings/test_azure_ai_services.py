import pytest
from pydantic import ValidationError
from src.settings.azure_ai_services import AzureAIServices


class TestAzureAIServices:
    """Unit tests for AzureAIServices settings."""

    def test_settings(self) -> None:
        """Test that Azure AI Services settings are being loaded as expected."""
        settings = AzureAIServices()

        assert settings.api_key == "test_ai_services_api_key"
        assert settings.endpoint == "test_ai_services_endpoint"
        assert settings.region == "test_ai_services_region"
        assert settings.audio_path == "test_audio_path"

    def test_settings_immutability(self) -> None:
        """Ensure settings are immutable after creation."""
        settings = AzureAIServices()
        with pytest.raises(ValidationError):
            settings.api_key = "new_ai_services_api_key"
