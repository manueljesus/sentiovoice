import pytest
from pydantic import ValidationError
from src.dtos.health_response import HealthResponse


class TestHealthModel:
    """
    Unit tests for Health DTO.
    """

    def test_valid_health(self):
        health_instance = HealthResponse(
            azure_open_ai_client=True,
            azure_text_analytics_client=True,
            azure_speech_synthesis_client=True,
        )

        assert health_instance.azure_open_ai_client
        assert health_instance.azure_text_analytics_client
        assert health_instance.azure_speech_synthesis_client

    def test_missing_field(self):
        with pytest.raises(ValidationError) as exc_info:
            HealthResponse()
        assert "type=missing" in str(exc_info.value)
