import pytest
from pydantic import ValidationError
from src.settings.azure_openai import AzureOpenAI


class TestAzureOpenAI:
    """Unit tests for AzureOpenAI settings."""

    def test_settings(self) -> None:
        """Test that Azure OpenAI settings are being loaded as expected."""
        settings = AzureOpenAI()

        assert settings.api_key == "test_openai_api_key"
        assert settings.deployment == "test_openai_deployment"
        assert settings.model == "test_openai_model"
        assert settings.api_version == "test_api_version"
        assert settings.endpoint == "test_openai_endpoint"
        assert settings.temperature == 0.7
        assert settings.max_tokens == 50
        assert settings.system_prompt == "test_system_prompt"

    def test_settings_immutability(self) -> None:
        """Ensure settings are immutable after creation."""
        settings = AzureOpenAI()
        with pytest.raises(ValidationError):
            settings.api_key = "new_openai_api_key"
