import streamlit as st

from src.audio import Audio, audio
from src.api_client import APIClient, api_client


class Feedback():
    """
    Process the user feedback, display the sentiment, AI-generated response, and handle audio output.
    """
    def __init__(self):
        self.api_client: APIClient = api_client
        self.audio: Audio = audio
        self.colors = {
            "POSITIVE": "#1B5E20",  # Green
            "NEGATIVE": "#B71C1C",  # Red
            "NEUTRAL": "#0D47A1",   # Blue
        }

    def process_feedback(
        self,
        feedback: str
    ) -> None:
        """
        Processes the user feedback by sending it to the API, displaying the sentiment,
        LLM-generated response, and handling the audio output.

        Args:
            feedback (str): The user's feedback text.
        """
        self.audio.clear()

        try:
            with st.spinner("Processing feedback..."):
                response = self.api_client.post_feedback(feedback)
                response.raise_for_status()
        except Exception:
            st.error("Error processing feedback. Please try again.")
            return

        result = response.json()

        self.display_sentiment(result.get('sentiment', 'NEUTRAL').upper())

        st.write(result.get('response', 'No response provided.'))

        self._process_audio(result.get('audio', ''))

    def submit_feedback(self):
        """
        Callback function that stores the text area input into session state
        and sets the submitted flag.
        """
        st.session_state.submitted = True
        st.session_state.feedback_input = st.session_state.feedback_box

    def display_sentiment(
        self,
        sentiment: str
    ) -> None:
        """
        Displays the sentiment feedback in a colored box without rounded corners.

        Args:
            sentiment (str): The sentiment text (e.g., "positive", "negative", "neutral").
        """
        color = self.colors.get(sentiment.upper(), "NEUTRAL")
        st.markdown(
            f"""
            <div style="
                padding: 10px;
                background-color: {color};
                text-align: center;
                font-weight: bold;
            ">
                {sentiment.capitalize()} feedback.
            </div>
            """,
            unsafe_allow_html=True
        )

    def _process_audio(
        self,
        audio_filename: str
    ):
        """
        Downloads and plays the audio file from the API response.

        Args:
            audio_filename (str): Audio filename.
        """
        if audio_filename:
            audio_path = self.audio.download(audio_filename)
            if audio_path:
                self.audio.play(audio_filename)
            else:
                st.warning("Audio file could not be downloaded.")
        else:
            st.info("No audio file returned by the API.")


feedback = Feedback()
