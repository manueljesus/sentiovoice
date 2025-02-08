from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


class AzureAIServices(BaseSettings):
    api_key: str = Field(
        alias=AliasChoices("AZURE_AI_SERVICES_API_KEY"), description="Azure AI Services API key"
    )

    endpoint: str = Field(
        alias=AliasChoices("AZURE_AI_SERVICES_ENDPOINT"), description="Azure AI Services endpoint"
    )

    region: str = Field(
        alias=AliasChoices("AZURE_AI_SERVICES_REGION"), description="Azure AI Services region"
    )

    model_config = SettingsConfigDict(env_file=".env", frozen=True, extra="ignore")
