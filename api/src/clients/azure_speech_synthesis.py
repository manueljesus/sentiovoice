import logging
from uuid_extensions import uuid7str

from azure.cognitiveservices.speech import (
    SpeechSynthesizer,
    SpeechConfig,
    SpeechSynthesisOutputFormat,
    AudioConfig,
    SpeechSynthesisResult,
    ResultReason,
)

from src import api_settings
from src.settings.azure_ai_services import AzureAIServices
from src.clients.client_errors import AzureSpeechSynthesisClientError

logger = logging.getLogger(__name__)


class AzureSpeechSynthesisClient:
    """
    Azure Speech Synthesis client.

    Attributes:
        client: TextAnalyticsClient: Azure Text Analytics client
    """

    def __init__(self):
        self.config = self._get_speech_config(api_settings.azure_ai_services)

    def __call__(self, text: str) -> str:
        filename = f"{uuid7str()}.mp3"

        synthesizer = SpeechSynthesizer(
            speech_config=self.config, audio_config=AudioConfig(filename=filename)
        )

        try:
            result: SpeechSynthesisResult = synthesizer.speak_text(text)
        except Exception as e:
            error = f"Speech synthesis failed: {e}"
            logger.error(error)
            raise AzureSpeechSynthesisClientError(error)

        if result.reason != ResultReason.SynthesizingAudioCompleted:
            error = "Speech synthesis failed"
            logger.error(error)
            raise AzureSpeechSynthesisClientError(error)

        return filename

    def _get_speech_config(self, settings: AzureAIServices) -> SpeechConfig:
        """
        Get the Azure Text Analytics client.

        Args:
            settings (AzureAIServices): Azure AI Services settings

        Returns:
            SpeechConfig: Azure AI Speech Config
        """
        speech_config = SpeechConfig(
            subscription=settings.api_key,
            region=settings.region,
        )

        speech_config.set_speech_synthesis_output_format(
            SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3
        )

        return speech_config


azure_speech_synthesis_client = AzureSpeechSynthesisClient()
