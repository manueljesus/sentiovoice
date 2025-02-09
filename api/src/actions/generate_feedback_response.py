from src.clients import (
    azure_openai_client,
    azure_text_analytics_client,
    azure_speech_synthesis_client,
)
from src.dtos import Feedback, SentimentResponse
from src.utils import Prompt


class GenerateFeedbackResponse:
    def __call__(self, feedback: Feedback) -> SentimentResponse:
        sentiment = azure_text_analytics_client.analyze_sentiment(feedback.feedback)
        feedback_response = azure_openai_client(
            Prompt()(sentiment, feedback.feedback)
        )
        audio_file = azure_speech_synthesis_client(feedback_response)

        return SentimentResponse(
            feedback=feedback.feedback,
            response=feedback_response,
            sentiment=sentiment,
            audio=audio_file,
        )
