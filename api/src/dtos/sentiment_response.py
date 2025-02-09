from pydantic import BaseModel


class SentimentResponse(BaseModel):
    feedback: str
    sentiment: str
    response: str
    audio: str
