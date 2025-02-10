from typing import Generator
from unittest.mock import patch, MagicMock

import pytest
import streamlit as st

from src.ui import UI


class TestUI:
    """ Test suite for the UI module. """
    @pytest.fixture
    def mock_submit_feedback(self) -> Generator[MagicMock, None, None]:
        with patch("src.feedback.feedback.submit_feedback") as mock:
            yield mock

    @pytest.fixture
    def mock_process_feedback(self) -> Generator[MagicMock, None, None]:
        with patch("src.feedback.feedback.process_feedback") as mock:
            yield mock

    @pytest.fixture
    def mock_display_sentiment(self) -> Generator[MagicMock, None, None]:
        with patch("src.feedback.feedback.display_sentiment") as mock:
            yield mock

    @pytest.fixture
    def mock_streamlit(self) -> Generator[MagicMock, None, None]:
        with patch("streamlit.markdown"), \
            patch("streamlit.title"), \
            patch("streamlit.write"), \
            patch("streamlit.subheader"), \
            patch("streamlit.text_area"), \
            patch("streamlit.warning"), \
            patch("streamlit.form_submit_button") as mock_form_submit_button:
            yield mock_form_submit_button

    @pytest.fixture()
    def ui(self) -> UI:
        return UI()

    def test_render_app_submit_feedback(
        self,
        mock_submit_feedback: MagicMock,
        mock_display_sentiment: MagicMock,
        mock_streamlit: MagicMock,
        ui: UI
    ):
        mock_form_submit_button = mock_streamlit

        # Simulate session state
        st.session_state["feedback_input"] = "Great app!"
        st.session_state["sentiment"] = "POSITIVE"

        ui.feedback.submit_feedback()

        ui.render_app()

        mock_display_sentiment.assert_called_once_with("POSITIVE")
        mock_submit_feedback.assert_called_once()
        mock_form_submit_button.assert_called_once_with(
            "Submit feedback",
            on_click=ui.feedback.submit_feedback,
            disabled=False
        )

    def test_render_app_already_rendered_feedback(
        self,
        mock_process_feedback: MagicMock,
        mock_streamlit: MagicMock,
        ui: UI
    ):
        # Simulate session state with submitted feedback
        st.session_state["submitted"] = True
        st.session_state["feedback_input"] = "Great app!"

        ui.render_app()

        mock_process_feedback.assert_called_once_with("Great app!")
        assert st.session_state["submitted"] is False

    def test_render_app_no_feedback_warning(
        self,
        mock_streamlit: MagicMock,
        ui: UI
    ):
        # Simulate empty feedback submission
        st.session_state["submitted"] = True
        st.session_state["feedback_input"] = ""

        with patch("streamlit.warning") as mock_warning:
            ui.render_app()
            mock_warning.assert_called_once_with("Please enter some feedback before submitting.")

    def test_render_app_disable_submit_button_if_no_change(
        self,
        mock_streamlit: MagicMock,
        ui: UI
    ):
        # Simulate no change in feedback input
        st.session_state["feedback_box"] = "Great app!"
        st.session_state["feedback_input"] = "Great app!"

        with patch("streamlit.form_submit_button") as mock_form_submit_button:
            ui.render_app()
            mock_form_submit_button.assert_called_once_with(
                "Submit feedback",
                on_click=ui.feedback.submit_feedback,
                disabled=True
            )
