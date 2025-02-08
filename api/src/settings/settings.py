from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.settings.azure_openai import AzureOpenAI


class Settings(BaseSettings):
    """
    Application settings
    """

    azure_openai: AzureOpenAI = Field(default_factory=AzureOpenAI)

    model_config = SettingsConfigDict(env_file=".env", frozen=True, extra="ignore")


api_settings = Settings()
