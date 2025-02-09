import pytest
from typing import Generator
from unittest.mock import MagicMock, patch
import streamlit as st

from src.app import main
from src.ui import ui


class TestApp:
    """Test suite for the app module."""
    @pytest.fixture
    def mock_set_page_config(self) -> Generator[MagicMock, None, None]:
        with patch.object(st, "set_page_config") as mock:
            yield mock

    @pytest.fixture
    def mock_render_app(self) -> Generator[MagicMock, None, None]:
        with patch.object(ui, "render_app") as mock:
            yield mock

    def test_main(
        self,
        mock_set_page_config: MagicMock,
        mock_render_app: MagicMock
    ):
        main()

        mock_set_page_config.assert_called_once_with(
            page_title="SentioVoice",
            page_icon="🔊",
            layout="centered",
            initial_sidebar_state="collapsed",
        )

        mock_render_app.assert_called_once()
