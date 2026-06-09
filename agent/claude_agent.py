from typing import Any

from anthropic import Anthropic

from config.config import Settings
from logger.logger import AppLogger


class ClaudeAgent:

    def __init__(self, model_name: str = "claude-haiku-4-5-20251001") -> None:

        self._model_name: str = model_name
        self._config: Settings = Settings()

        self._client: Anthropic = Anthropic(api_key=self._config.claude_api_key)

        self._logger = AppLogger.get_logger(self.__class__.__name__)

    def test_method(self) -> None:

        user_prompt_str: str = "Tell me the current date / time in the format YYYY-MM-YY HH:MM:SS"

        messages: list[dict[str, Any]] = [
            {"role": "user", "content": user_prompt_str}
        ]

        try:
            response = self._client.messages.create(
                model=self._model_name,
                max_tokens=256,
                # tools=self.tools.get_tool_schemas(),
                messages=messages
            )

            self._logger.info(f"response.content[0].text = {response.content[0].text}")


        except Exception as e:
            self._logger.error(f"Exception Thrown: {e}")
            raise Exception
