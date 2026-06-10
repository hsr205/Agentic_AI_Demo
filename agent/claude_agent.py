import json
import sys
from typing import Any

from anthropic import Anthropic
from mcp import StdioServerParameters, stdio_client, ClientSession

from agent_tools.email_notification_dispatch import EmailNotificationDispatcher
from config.config import Settings
from logger.logger import AppLogger


class ClaudeAgent:

    def __init__(self) -> None:

        self._config: Settings = Settings()

        self._model_name: str = self._config.claude_model_name
        self._client: Anthropic = Anthropic(api_key=self._config.claude_api_key)

        self._email_notification_dispatcher: EmailNotificationDispatcher = EmailNotificationDispatcher()

        self._logger = AppLogger.get_logger(self.__class__.__name__)

    async def run_pipeline(self, user_prompt: str) -> None:
        """Establishes an active connection link to an external MCP capability server,

        exposes its tools to Claude, and handles responses natively.
        """
        server_parameters = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_server.ticket_mcp_server"]
        )

        self._logger.info("Initializing secure stdio transport link to MCP Server...")

        try:
            async with stdio_client(server_parameters) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:

                    # Automatically complete the protocol handshake sync
                    await session.initialize()
                    self._logger.info("Handshake completed successfully.")

                    mcp_tools_payload = await session.list_tools()

                    claude_compatible_tools: list[dict[str, Any]] = [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "input_schema": tool.inputSchema
                        }
                        for tool in mcp_tools_payload.tools
                    ]

                    # Initialize the clean stateless conversation message list
                    conversation_history: list[dict[str, Any]] = [
                        {"role": "user", "content": user_prompt}
                    ]

                    self._logger.info("Dispatching state payload to Anthropic...")


                    response = self._client.messages.create(
                        model=self._model_name,
                        max_tokens=1000,
                        tools=claude_compatible_tools,
                        messages=conversation_history
                    )

                    if response.stop_reason == "tool_use":
                        for block in response.content:
                            if block.type == "tool_use":
                                self._logger.info(f"Routing request to tool: '{block.name}'")

                                tool_execution_yield = await session.call_tool(
                                    name=block.name,
                                    arguments=block.input
                                )

                                raw_content_str: str = tool_execution_yield.content[0].text
                                raw_content_list:list[dict] = json.loads(raw_content_str)

                                if len(raw_content_list) > 0:
                                    self._logger.info("Target deals encountered. Firing SMTP.")
                                    self._email_notification_dispatcher.execute_email_ticket_notification(
                                        matched_events=raw_content_list
                                    )
                                else:
                                    self._logger.info("Yield was empty. SMTP skipped.")
        except Exception as e:
            self._logger.error(f"[CRITICAL BOUNDARY FAILURE]: {e}")
            raise e
