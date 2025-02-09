import yaml

from src import api_settings


class Prompt:
    def __init__(self):
        self.prompts = self._load_prompts()

    def __call__(self, sentiment: str, feedback_text: str) -> str:
        """
        Generates a prompt for the LLM based on the sentiment extracted from the feedback.

        Args:
            sentiment (str): Either "POSITIVE", "NEGATIVE", or "NEUTRAL"
            feedback_text (str): User's feedback text

        Returns:
            str: The formatted prompt for the LLM to generate a response to the feedback and sentiment.
        """
        return self._get_formatted_prompt(sentiment, feedback_text)

    def _load_prompts(self):
        """Loads LLM prompts from a YAML file."""
        with open(f"{api_settings.prompt}.yaml", "r") as file:
            prompts = yaml.safe_load(file)
        return prompts["llm_prompts"]

    def _get_formatted_prompt(
        self,
        sentiment: str,
        feedback_text: str,
    ) -> str:
        """Formats the prompt with the provided sentiment and feedback text."""
        prompt_template = self.prompts.get(sentiment, self.prompts["NEUTRAL"])
        return prompt_template.format(feedback_text=feedback_text)
