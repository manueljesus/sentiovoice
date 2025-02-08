import pytest
from pydantic import ValidationError
from src.settings.settings import Settings
from src.settings.azure_openai import AzureOpenAI


class TestSettings:
    """Unit tests for the API settings."""

    def test_settings(self) -> None:
        """Test that the API settings are being loaded as expected."""
        settings = Settings()
        assert isinstance(settings.azure_openai, AzureOpenAI)

    def test_settings_immutability(self) -> None:
        """Ensure settings are immutable after creation."""
        settings = Settings()
        with pytest.raises(ValidationError):
            settings.azure_openai = "invalid_value"
