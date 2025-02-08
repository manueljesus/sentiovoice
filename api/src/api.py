from fastapi import FastAPI
from fastapi.responses import RedirectResponse

api = FastAPI(
    title="SentioVoice API",
    description="An API for sentiment analysis, LLM response generation, and speech synthesis.",
    version="0.1.0",
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)


@api.get("/")
def root():
    """
    Redirects to the API documentation.

    Returns:
        RedirectResponse: Redirects to the API documentation.
    """

    return RedirectResponse(url="/docs")
