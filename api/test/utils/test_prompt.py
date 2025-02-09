import pytest
from unittest.mock import MagicMock, patch, mock_open
from src.utils.prompt import Prompt
import yaml


class TestPrompt:
    """
    Prompt retrieval utility tests.
    """
    @pytest.fixture
    def mock_prompts_dict(self):
        """
        Mocked _load_prompts() data.
        """
        return {
            "POSITIVE": "Positive: {feedback_text}",
            "NEGATIVE": "Negative: {feedback_text}",
            "NEUTRAL": "Neutral: {feedback_text}",
        }

    @pytest.fixture
    def mock_file_load(self, mock_prompts_dict):
        """
        Patches 'open' so that any attempt to open a file in 'src.utils.prompt'
        will read from a mock YAML string instead of disk.
        """
        mock_yaml_dict = {"llm_prompts": mock_prompts_dict}
        mock_yaml_str = yaml.safe_dump(mock_yaml_dict)

        with patch("src.utils.prompt.open", mock_open(read_data=mock_yaml_str)) as mocked_file:
            yield mocked_file

    @pytest.mark.parametrize(
        "sentiment, feedback_text, expected",
        [
            ("POSITIVE", "Great job!", "Positive: Great job!"),
            ("NEGATIVE", "Not good!", "Negative: Not good!"),
            ("NEUTRAL", "Just okay.", "Neutral: Just okay."),
            ("OTHER", "Random feedback", "Neutral: Random feedback"),
        ],
    )
    def test_prompt_call(
        self,
        mock_file_load: MagicMock,
        sentiment: str,
        feedback_text: str,
        expected: str
    ):
        assert Prompt()(sentiment, feedback_text) == expected
