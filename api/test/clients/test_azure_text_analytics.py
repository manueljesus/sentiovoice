import logging
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from azure.ai.textanalytics import AnalyzeSentimentResult, DocumentError
from azure.core.exceptions import HttpResponseError, ClientAuthenticationError

from src.clients import azure_text_analytics_client
from src.clients.client_errors import AzureTextAnalyticsClientError
from src.clients.azure_text_analytics import AzureTextAnalyticsClient


class TestAzureTextAnalyticsClient:
    @pytest.fixture
    def mock_text_analytics_client(self):
        """Fixture to mock the Azure Text Analytics client."""
        with patch(
            "src.clients.azure_text_analytics.AzureTextAnalyticsClient._get_text_analytics_client"
        ) as mock_client:
            yield mock_client

    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock the logger."""
        with patch.object(
            logging.getLogger("src.clients.azure_text_analytics"), "error"
        ) as mock_log_error:
            yield mock_log_error

    @pytest.fixture
    def text_analytics_client(
        self, mock_text_analytics_client: MagicMock
    ) -> AzureTextAnalyticsClient:
        """Fixture to create an instance of AzureTextAnalyticsClient with a mock."""
        return AzureTextAnalyticsClient()

    def test_successful_response(
        self,
        text_analytics_client: AzureTextAnalyticsClient,
        mock_text_analytics_client: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test successful response from AzureTextAnalyticsClient."""
        mock_response = MagicMock(spec=AnalyzeSentimentResult)
        mock_response.sentiment = "positive"
        mock_text_analytics_client.return_value.analyze_sentiment.return_value = [
            mock_response
        ]

        sentiment = text_analytics_client.analyze_sentiment("I love programming!")

        assert sentiment == "POSITIVE"
        mock_text_analytics_client.return_value.analyze_sentiment.assert_called_once()
        mock_logger.assert_not_called()

    def test_neutral_sentiment_response(
        self,
        text_analytics_client: AzureTextAnalyticsClient,
        mock_text_analytics_client: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test handling of neutral sentiment response."""
        mock_response = MagicMock(spec=AnalyzeSentimentResult)
        mock_response.sentiment = "mixed"
        mock_text_analytics_client.return_value.analyze_sentiment.return_value = [
            mock_response
        ]

        sentiment = text_analytics_client.analyze_sentiment("It's okay, I guess.")

        assert sentiment == "NEUTRAL"
        mock_text_analytics_client.return_value.analyze_sentiment.assert_called_once()
        mock_logger.assert_not_called()

    def test_document_error_response(
        self,
        text_analytics_client: AzureTextAnalyticsClient,
        mock_text_analytics_client: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test handling of DocumentError response."""
        mock_error = MagicMock(spec=DocumentError)
        mock_text_analytics_client.return_value.analyze_sentiment.return_value = [
            mock_error
        ]

        with pytest.raises(
            AzureTextAnalyticsClientError, match="Text Analytics API error"
        ):
            text_analytics_client.analyze_sentiment("Bad input")

        mock_logger.assert_called_once_with("Text Analytics API error")

    def test_http_response_error(
        self,
        text_analytics_client: AzureTextAnalyticsClient,
        mock_text_analytics_client: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test handling of HTTP response errors."""
        mock_text_analytics_client.return_value.analyze_sentiment.side_effect = (
            HttpResponseError("Service unavailable")
        )

        with pytest.raises(
            AzureTextAnalyticsClientError,
            match="Text Analytics API error: Service unavailable",
        ):
            text_analytics_client.analyze_sentiment("Some text")

        mock_logger.assert_called_once_with(
            "Text Analytics API error: Service unavailable"
        )

    def test_authentication_error(
        self,
        text_analytics_client: AzureTextAnalyticsClient,
        mock_text_analytics_client: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test handling of authentication errors."""
        mock_text_analytics_client.return_value.analyze_sentiment.side_effect = (
            ClientAuthenticationError("Invalid API Key")
        )

        with pytest.raises(
            AzureTextAnalyticsClientError,
            match="Text Analytics API error: Invalid API Key",
        ):
            text_analytics_client.analyze_sentiment("Test prompt")

        mock_logger.assert_called_once_with("Text Analytics API error: Invalid API Key")

    def test_unexpected_exception(
        self,
        text_analytics_client: AzureTextAnalyticsClient,
        mock_text_analytics_client: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test handling of unexpected exceptions."""
        mock_text_analytics_client.return_value.analyze_sentiment.side_effect = (
            Exception("Unexpected failure")
        )

        with pytest.raises(
            AzureTextAnalyticsClientError,
            match="Text Analytics API error: Unexpected failure",
        ):
            text_analytics_client.analyze_sentiment("Test prompt")

        mock_logger.assert_called_once_with(
            "Text Analytics API error: Unexpected failure"
        )

    def test_sentiment_processing_exception(
        self,
        text_analytics_client: AzureTextAnalyticsClient,
        mock_text_analytics_client: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test exception handling when processing sentiment result."""
        mock_response = MagicMock(spec=AnalyzeSentimentResult)
        del mock_response.sentiment  # Simulate missing sentiment attribute
        mock_text_analytics_client.return_value.analyze_sentiment.return_value = [
            mock_response
        ]

        with pytest.raises(
            AzureTextAnalyticsClientError, match="Sentiment analysis failed"
        ):
            text_analytics_client.analyze_sentiment("I love coding!")

        mock_logger.assert_called_once()

    def test_singleton_instance(self):
        """Test that the module-initialized AzureTextAnalyticsClient is a singleton."""

        assert azure_text_analytics_client is azure_text_analytics_client
