from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.settings.azure_openai import AzureOpenAI
from src.settings.azure_ai_services import AzureAIServices


class Settings(BaseSettings):
    """
    Application settings
    """

    azure_openai: AzureOpenAI = Field(default_factory=AzureOpenAI)
    azure_ai_services: AzureAIServices = Field(default_factory=AzureAIServices)

    model_config = SettingsConfigDict(env_file=".env", frozen=True, extra="ignore")


api_settings = Settings()
