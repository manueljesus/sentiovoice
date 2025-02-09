import pytest
from pydantic import ValidationError
from src.settings import Settings


class TestSettings:
    """Unit tests for the UI settings."""

    def test_settings(self) -> None:
        """Test that the UI settings are being loaded as expected."""
        settings = Settings()
        assert settings.api_url == "test_api_url"
        assert settings.audio_path == "test_audio_path"

    def test_settings_immutability(self) -> None:
        """Ensure settings are immutable after creation."""
        settings = Settings()
        with pytest.raises(ValidationError):
            settings.azure_openai = "invalid_value"
