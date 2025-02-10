import os
import streamlit as st
from typing import Union

from src.api_client import APIClient, api_client
from src.settings import settings


class Audio():
    def __init__(self):
        self.audio_dir = settings.audio_path
        self.api_client: APIClient = api_client

    def clear(self):
        """
        Deletes the existing audio files in the local folder.
        """

        if os.path.exists(self.audio_dir):
            for file in os.listdir(self.audio_dir):
                file_path = os.path.join(self.audio_dir, file)
                os.remove(file_path)
        else:
            os.makedirs(self.audio_dir)

    def download(
        self,
        filename: str
    ) -> Union[str, None]:
        """
        Downloads the audio file from the API and saves it locally.
        """

        response = self.api_client.get_audio(filename)

        audio_path = self._audio_file(filename)

        if response.status_code == 200:
            with open(audio_path, "wb") as audio_file:
                audio_file.write(response.content)
            return audio_path
        else:
            st.error("Failed to download the audio file.")
            return None

    def play(
        self,
        audio_filename: str
    ):
        """
        Plays the downloaded audio file from the local directory.
        """

        audio_path = self._audio_file(audio_filename)

        if os.path.exists(audio_path):
            with open(audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")
        else:
            st.error("Audio file not found.")

    def _audio_file(self, audio_filename: str):
        """Returns the audio file path."""
        return os.path.join(self.audio_dir, audio_filename)


audio = Audio()
