from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings
    """

    api_url: str = Field(
        alias=AliasChoices("API_URL"), description="API URL"
    )

    audio_path: str = Field(
        alias=AliasChoices("AUDIO_PATH"),
        description="Path to save and retrieve audio files",
        default="audio",
    )

    model_config = SettingsConfigDict(env_file=".env", frozen=True, extra="ignore")


settings = Settings()
