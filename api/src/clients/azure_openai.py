import logging
from typing import List

from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_openai import AzureChatOpenAI

from src import api_settings
from src.settings.azure_openai import AzureOpenAI
from src.clients.client_errors import AzureOpenAIClientError

logger = logging.getLogger(__name__)


class AzureOpenAIClient:
    """
    Azure OpenAI client for interacting with the Azure OpenAI API.

    Attributes:
        client (AzureChatOpenAI): An instance of the AzureChatOpenAI client.
        system_prompt (str): The system prompt to be prepended to each call.
    """

    def __init__(self, system_prompt: str):
        """
        Initialize the Azure OpenAI client with the provided system prompt.

        Args:
            system_prompt (str): The system prompt to be prepended to each call.
        """
        self.client: AzureChatOpenAI = self._get_openai_client(
            api_settings.azure_openai
        )
        self.system_prompt = system_prompt

    def __call__(self, prompt: str) -> str:
        """
        Send a prompt to the Azure OpenAI API and return the processed response.

        Args:
            prompt (str): The user's prompt message.

        Returns:
            str: The API response content after stripping any leading/trailing whitespace.
        """
        messages: List = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt),
        ]

        try:
            response: AIMessage = self.client.invoke(messages)

            return response.content.strip()
        except Exception as e:
            error_message = f"LLM response generation failed: {e}"
            logger.error(error_message)
            raise AzureOpenAIClientError(error_message)

    def _get_openai_client(self, settings: AzureOpenAI) -> AzureChatOpenAI:
        """
        Instantiate and return an AzureChatOpenAI client using the provided settings.

        Args:
            settings (AzureOpenAI): The settings object containing API configuration details.

        Returns:
            AzureChatOpenAI: An instantiated AzureChatOpenAI client.
        """
        return AzureChatOpenAI(
            api_key=settings.api_key,
            azure_deployment=settings.deployment,
            model=settings.model,
            api_version=settings.api_version,
            azure_endpoint=settings.endpoint,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )
