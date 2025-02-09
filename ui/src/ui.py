import streamlit as st
from src.feedback import feedback


class UI:
    def __init__(self):
        self.feedback = feedback

    def render_app(self) -> None:
        """
        Renders the main application UI, including the feedback form.
        """

        # Hide the Streamlit menu, header, and footer
        hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        st.title("SentioVoice")
        st.write("Feedback Sentiment Analyzer")
        st.subheader("Giving voice to your feedback")

        st.text_area("Enter your feedback here:", key="feedback_box")

        with st.form("feedback_form", clear_on_submit=False, border=False):
            if "sentiment" in st.session_state:
                self.feedback.display_sentiment(st.session_state.sentiment)
            st.form_submit_button(
                "Submit feedback",
                on_click=self.feedback.submit_feedback,
                disabled=st.session_state.get("feedback_box", "").strip()
                == st.session_state.get("feedback_input", "").strip(),
            )

        if "submitted" in st.session_state and st.session_state.submitted:
            st.session_state.submitted = False
            feedback_text = st.session_state.get("feedback_input", "").strip()
            if feedback_text:
                self.feedback.process_feedback(feedback_text)
            else:
                st.warning("Please enter some feedback before submitting.")


ui = UI()
