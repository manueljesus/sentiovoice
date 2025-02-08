from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


class AzureOpenAI(BaseSettings):
    api_key: str = Field(
        alias=AliasChoices("AZURE_OPENAI_API_KEY"), description="Azure OpenAI API key"
    )

    deployment: str = Field(
        alias=AliasChoices("AZURE_OPENAI_DEPLOYMENT"),
        description="Azure OpenAI deployment",
    )

    model: str = Field(
        alias=AliasChoices("AZURE_OPENAI_MODEL"), description="Azure OpenAI model"
    )

    api_version: str = Field(
        alias=AliasChoices("AZURE_OPENAI_API_VERSION"),
        description="Azure OpenAI API version",
    )

    endpoint: str = Field(
        alias=AliasChoices("AZURE_OPENAI_ENDPOINT"), description="Azure OpenAI endpoint"
    )

    temperature: float = Field(
        alias=AliasChoices("AZURE_OPENAI_TEMPERATURE"),
        description="Azure OpenAI temperature",
    )

    max_tokens: int = Field(
        alias=AliasChoices("AZURE_OPENAI_MAX_TOKENS"),
        description="Azure OpenAI max tokens",
    )

    model_config = SettingsConfigDict(env_file=".env", frozen=True, extra="ignore")
