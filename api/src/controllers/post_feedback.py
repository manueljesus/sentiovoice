from fastapi import APIRouter, Body
from src.actions import GenerateFeedbackResponse
from src.dtos import Feedback, SentimentResponse

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post(
    "/",
    response_model=SentimentResponse,
    summary="Process user feedback",
    description="Analyzes feedback sentiment and generates an AI response including audio.",
    response_description="The analyzed sentiment, generated response, and corresponding audio file.",
)
def process_feedback(
    feedback: Feedback = Body(..., examples=[{"feedback": "This is a great product!"}]),
) -> SentimentResponse:
    return GenerateFeedbackResponse()(feedback)
