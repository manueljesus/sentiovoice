import os
import logging
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from azure.cognitiveservices.speech import SpeechSynthesisResult, ResultReason

from src.clients import azure_speech_synthesis_client
from src.clients.azure_speech_synthesis import AzureSpeechSynthesisClient
from src.clients.client_errors import AzureSpeechSynthesisClientError


class TestAzureSpeechSynthesisClient:
    @pytest.fixture
    def mock_speech_synthesizer(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock the Azure Speech Synthesizer."""
        with patch(
            "src.clients.azure_speech_synthesis.SpeechSynthesizer"
        ) as mock_synthesizer:
            yield mock_synthesizer

    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock the logger."""
        with patch.object(
            logging.getLogger("src.clients.azure_speech_synthesis"), "error"
        ) as mock_log_error:
            yield mock_log_error

    @pytest.fixture
    def mock_os_path_join(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock os.path.join."""
        with patch(
            "os.path.join", side_effect=lambda *args: "/".join(args)
        ) as mock_join:
            yield mock_join

    @pytest.fixture
    def speech_synthesis_client(
        self, mock_speech_synthesizer: MagicMock
    ) -> AzureSpeechSynthesisClient:
        """Fixture to create an instance of AzureSpeechSynthesisClient with a mock."""
        return AzureSpeechSynthesisClient()

    def test_successful_speech_synthesis(
        self,
        speech_synthesis_client: AzureSpeechSynthesisClient,
        mock_speech_synthesizer: MagicMock,
        mock_logger: MagicMock,
        mock_os_path_join: MagicMock,
    ):
        """Test successful speech synthesis."""
        mock_result = MagicMock(spec=SpeechSynthesisResult)
        mock_result.reason = ResultReason.SynthesizingAudioCompleted
        mock_speech_synthesizer.return_value.speak_text.return_value = mock_result

        filename = speech_synthesis_client("Hello")

        assert filename.endswith(".mp3")
        mock_logger.assert_not_called()
        mock_os_path_join.assert_called_once()

    def test_speech_synthesis_api_failure(
        self,
        speech_synthesis_client: AzureSpeechSynthesisClient,
        mock_speech_synthesizer: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test handling when the API call fails."""
        mock_speech_synthesizer.return_value.speak_text.side_effect = Exception(
            "API Error"
        )

        with pytest.raises(
            AzureSpeechSynthesisClientError, match="Speech synthesis failed: API Error"
        ):
            speech_synthesis_client("Hello")

        mock_logger.assert_called_once_with("Speech synthesis failed: API Error")

    def test_speech_synthesis_unsuccessful(
        self,
        speech_synthesis_client: AzureSpeechSynthesisClient,
        mock_speech_synthesizer: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test handling when speech synthesis does not complete successfully."""
        mock_result = MagicMock(spec=SpeechSynthesisResult)
        mock_result.reason = ResultReason.Canceled  # Simulate a failure
        mock_speech_synthesizer.return_value.speak_text.return_value = mock_result

        with pytest.raises(
            AzureSpeechSynthesisClientError, match="Speech synthesis failed"
        ):
            speech_synthesis_client("Hello")

        mock_logger.assert_called_once_with("Speech synthesis failed")

    def test_singleton_instance(self):
        """Test that the module-initialized AzureSpeechSynthesisClient is a singleton."""

        assert azure_speech_synthesis_client is azure_speech_synthesis_client
