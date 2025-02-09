import requests

from src.settings import settings


class APIClient():
    def __init__(self):
        self.api_url = settings.api_url

    def post_feedback(
        self,
        feedback: str
    ) -> requests.Response:
        """
        Send the feedback to the API.

        Args:
            feedback (str): The feedback message.

        Returns:
            requests.Response: The response from the API.
            {
                "feedback": "The feedback message."
                "sentiment": "The sentiment of the feedback."
                "response": "The response to the feedback."
                "audio": "The synthesized response audio file."
            }
        """
        feedback_url = f"{self.api_url}/feedback"
        response = requests.post(feedback_url, json={"feedback": feedback})
        return response

    def get_audio(
        self,
        filename: str
    ) -> requests.Response:
        """
        Download the audio file from the API.

        Args:
            audio_filename (str): The audio file name.

        Returns:
            requests.Response: The response from the API with the audio file.
        """
        audio_url = f"{self.api_url}/audio/{filename}"
        response = requests.get(audio_url)
        return response


api_client = APIClient()
