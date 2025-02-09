import streamlit as st


def main() -> None:
    """ Streamlit entrypoint """
    st.set_page_config(
        page_title="SentioVoice",
        page_icon="🔊",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
