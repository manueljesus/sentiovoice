from fastapi import APIRouter, HTTPException

from src.clients.azure_openai import AzureOpenAIClient
from src.clients.azure_speech_synthesis import AzureSpeechSynthesisClient
from src.clients.azure_text_analytics import AzureTextAnalyticsClient
from src.dtos import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    summary="Health check",
    description="Checks the health of all Azure services clients.",
    response_description="The health status of all Azure services clients.",
    response_model=HealthResponse
)
def health_check():
    health_response = HealthResponse(
        azure_open_ai_client=_check_azure_openai_client(),
        azure_text_analytics_client=_check_azure_text_analytics_client(),
        azure_speech_synthesis_client=_check_azure_speech_synthesis_client(),
    )

    if not all(
        [
            health_response.azure_open_ai_client,
            health_response.azure_text_analytics_client,
            health_response.azure_speech_synthesis_client,
        ]
    ):
        raise HTTPException(
            status_code=500,
            detail={
                "message": "One or more Azure services are unavailable",
                "status": health_response.model_dump(),
            },
        )

    return health_response


def _check_azure_openai_client():
    try:
        AzureOpenAIClient()
        return True
    except Exception as e:
        print(f"AzureOpenAIClient init failed: {e}")
        return False


def _check_azure_text_analytics_client():
    try:
        AzureTextAnalyticsClient()
        return True
    except Exception as e:
        print(f"AzureTextAnalyticsClient init failed: {e}")
        return False


def _check_azure_speech_synthesis_client():
    try:
        AzureSpeechSynthesisClient()
        return True
    except Exception as e:
        print(f"AzureSpeechSynthesisClient init failed: {e}")
        return False
