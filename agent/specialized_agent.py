from anthropic import Anthropic

from logger.logger import AppLogger


class SpecializedAgent:

    def __init__(self, name_str: str, model_name_str: str, client: Anthropic, system_prompt: str) -> None:
        self.name: str = name_str
        self._client: Anthropic = client
        self._system_prompt: str = system_prompt
        self._model: str = model_name_str
        self._logger = AppLogger.get_logger(self.__class__.__name__)

    def execute_turn(self, prompt: str, schema_context: dict[str, str | dict[str, str | list[str]]],
                     context_data: str | None = None) -> str:
        """Runs an isolated evaluation turn using a pre-resolved structural tool schema context."""
        self._logger.info(f"[{self.name.upper()}] Waking up in isolated cognitive thread...")

        full_prompt: str = prompt
        if context_data:
            full_prompt += f"\n\nContext payload provided by Orchestrator:\n{context_data}"

        messages: list[dict[str, str]] = [{"role": "user", "content": full_prompt}]

        anthropic_formatted_tools = [schema_context]

        response = self._client.messages.create(
            model=self._model,
            max_tokens=1000,
            system=self._system_prompt,
            tools=anthropic_formatted_tools,
            messages=messages
        )

        output_text: str = ""
        for block in response.content:
            if block.type == "text":
                output_text += block.text
            elif block.type == "tool_use":
                self._logger.info(f"[{self.name.upper()}] Confirmed Tool Generation via Introspection: '{block.name}'")
                output_text += f"\n[Agent invoked tool {block.name} with args: {block.input}]"

        return output_text
