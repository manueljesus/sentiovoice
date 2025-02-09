from pydantic import BaseModel


class HealthResponse(BaseModel):
    azure_open_ai_client: bool
    azure_text_analytics_client: bool
    azure_speech_synthesis_client: bool
