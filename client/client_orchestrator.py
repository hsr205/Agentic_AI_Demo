import asyncio
from logging import Logger

from agent.claude_agent import ClaudeAgent
from logger.logger import AppLogger


class ClientOrchestrator:

    def __init__(self) -> None:
        self._agent: ClaudeAgent = ClaudeAgent()
        self._logger: Logger = AppLogger.get_logger(self.__class__.__name__)

    def execute_pipeline(self, prompt: str) -> int:

        self._logger.info("Initializing synchronous event loop runtime...")
        try:
            asyncio.run(self._agent.run_pipeline(user_prompt=prompt))
            self._logger.info("System pipeline context terminated cleanly.")
            return 0
        except Exception as critical_fault:
            self._logger.exception(f"[CRITICAL APPLICATION CRASH]: {critical_fault}")
            return -1
