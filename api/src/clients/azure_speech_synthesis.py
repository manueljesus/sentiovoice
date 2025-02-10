import os
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
        self.voices = {
            "POSITIVE": "excited",
            "NEUTRAL": "default",
            "NEGATIVE": "empathetic"
        }

    def __call__(self, text: str, sentiment: str = "NEUTRAL") -> str:
        audio_path = api_settings.azure_ai_services.audio_path

        os.makedirs(audio_path, exist_ok=True)

        filename = f"{uuid7str()}.mp3"
        file_path = os.path.join(audio_path, filename)

        synthesizer = SpeechSynthesizer(
            speech_config=self.config, audio_config=AudioConfig(filename=file_path)
        )

        ssml = self._generate_ssml(
            text,
            self.voices.get(sentiment.upper(), self.voices["NEUTRAL"])
        )

        try:
            result: SpeechSynthesisResult = synthesizer.speak_ssml(ssml)
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

    def _generate_ssml(self, text: str, style: str) -> str:
        """
        Generate SSML with sentiment styling.

        Args:
            text (str): The input text.
            style (str): The voice style to apply.

        Returns:
            str: SSML string.
        """
        ssml_template = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='en-US'>
            <voice name='en-US-AriaNeural'>
                <mstts:express-as style='{style}'>
                    {text}
                </mstts:express-as>
            </voice>
        </speak>
        """
        return ssml_template.strip()


azure_speech_synthesis_client = AzureSpeechSynthesisClient()
