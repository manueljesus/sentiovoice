from unittest.mock import patch
import streamlit as st

from src.app import main


class TestApp:
    """Test suite for the app module."""

    def test_main(self):
        with patch.object(st, "set_page_config") as mock_set_page_config:
            main()
            mock_set_page_config.assert_called_once_with(
                page_title="SentioVoice",
                page_icon="🔊",
                layout="centered",
                initial_sidebar_state="collapsed",
            )
