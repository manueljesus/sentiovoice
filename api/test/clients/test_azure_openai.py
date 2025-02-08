import pytest
import logging
from typing import Generator
from unittest.mock import MagicMock, patch
from langchain.schema import AIMessage

from src.clients import azure_openai_client
from src.clients.client_errors import AzureOpenAIClientError
from src.clients.azure_openai import AzureOpenAIClient


class TestAzureOpenAIClient:
    @pytest.fixture
    def mock_azure_chat_openai(self):
        """Fixture to mock AzureChatOpenAI client."""
        with patch("src.clients.azure_openai.AzureChatOpenAI") as mock_client:
            yield mock_client

    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """Fixture to mock the logger."""
        with patch.object(
            logging.getLogger("src.clients.azure_openai"), "error"
        ) as mock_log_error:
            yield mock_log_error

    @pytest.fixture
    def azure_openai_client(
        self, mock_azure_chat_openai: MagicMock
    ) -> AzureOpenAIClient:
        """Fixture to create an instance of AzureOpenAIClient with a mock."""
        mock_instance = mock_azure_chat_openai.return_value
        mock_instance.invoke.return_value = AIMessage(content="Mock response")
        return AzureOpenAIClient()

    def test_successful_response(
        self,
        azure_openai_client: AzureOpenAIClient,
        mock_azure_chat_openai: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test successful response from AzureOpenAIClient."""
        prompt = "Hello, how are you?"
        response = azure_openai_client(prompt)

        assert response == "Mock response"
        mock_azure_chat_openai.return_value.invoke.assert_called_once()
        mock_logger.assert_not_called()

    def test_exception_handling(
        self,
        azure_openai_client: AzureOpenAIClient,
        mock_azure_chat_openai: MagicMock,
        mock_logger: MagicMock,
    ):
        """Test exception handling when an API error occurs."""
        mock_azure_chat_openai.return_value.invoke.side_effect = Exception("API Error")

        with pytest.raises(
            AzureOpenAIClientError, match="LLM response generation failed: API Error"
        ):
            azure_openai_client("Test prompt")

        mock_logger.assert_called_once_with("LLM response generation failed: API Error")

    def test_singleton_instance(
        self
    ):
        """Test that the module-initialized AzureOpenAIClient is a singleton."""

        assert azure_openai_client is azure_openai_client
