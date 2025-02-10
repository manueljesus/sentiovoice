import logging

from typing import List

from azure.ai.textanalytics import (
    TextAnalyticsClient,
    AnalyzeSentimentResult,
    DocumentError
)
from azure.core.credentials import AzureKeyCredential

from src import api_settings
from src.settings.azure_ai_services import AzureAIServices
from src.clients.client_errors import AzureTextAnalyticsClientError

logger = logging.getLogger(__name__)


class AzureTextAnalyticsClient:
    """
    Azure Text Analytics client.

    Attributes:
        client: TextAnalyticsClient: Azure Text Analytics client
    """

    def __init__(self):
        self.client = self._get_text_analytics_client(api_settings.azure_ai_services)

    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze the sentiment of a given text.

        Args:
            text (str): The text to analyze

        Returns:
            str: The sentiment of the text
        """
        try:
            response: List[AnalyzeSentimentResult | DocumentError] = (
                self.client.analyze_sentiment(documents=[text])
            )
        except Exception as e:
            error = f"Text Analytics API error: {e}"
            logger.error(error)
            raise AzureTextAnalyticsClientError(error)

        if isinstance(response[0], DocumentError):
            error = "Text Analytics API error"
            logger.error(error)
            raise AzureTextAnalyticsClientError(error)

        try:
            sentiment = response[0].sentiment.upper()
            return sentiment if sentiment in ("POSITIVE", "NEGATIVE") else "NEUTRAL"
        except Exception as e:
            error = f"Sentiment analysis failed: {e}"
            logger.error(error)
            raise AzureTextAnalyticsClientError(error)

    def _get_text_analytics_client(
        self, settings: AzureAIServices
    ) -> TextAnalyticsClient:
        """
        Get the Azure Text Analytics client.

        Args:
            settings (AzureAIServices): Azure AI Services settings

        Returns:
            TextAnalyticsClient: Azure Text Analytics client
        """
        return TextAnalyticsClient(
            endpoint=settings.endpoint, credential=AzureKeyCredential(settings.api_key)
        )


azure_text_analytics_client = AzureTextAnalyticsClient()
