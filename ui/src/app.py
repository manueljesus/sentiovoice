import streamlit as st
from src.ui import ui


def main() -> None:
    """ Streamlit entrypoint """
    st.set_page_config(
        page_title="SentioVoice",
        page_icon="🔊",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    ui.render_app()
