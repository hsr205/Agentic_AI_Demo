from anthropic import Anthropic

from agent.specialized_agent import SpecializedAgent
from config.config import Settings
from logger.logger import AppLogger
from mcp_servers.finance_mcp_server import FinanceMCPServer


class AgentOrchestrator:

    def __init__(self) -> None:
        self._config: Settings = Settings()
        self._client: Anthropic = Anthropic(api_key=self._config.claude_api_key)
        self._mcp_server: FinanceMCPServer = FinanceMCPServer()

        # Initialize subagents with hyper-focused system prompts
        self._data_fetching_agent: SpecializedAgent = SpecializedAgent(
            name_str="Data_Fetching_Agent",
            client=self._client,
            model_name_str=self._config.claude_model_name,
            system_prompt="You are the Data Fetching / Downloading Analyst. Extract stock datat based on their dates, and use the download_historical_stock_data tool."
        )

        # self._data_aggregation_agent: SpecializedAgent = SpecializedAgent(
        #     name_str="Data_Aggregation_Agent",
        #     client=self._client,
        #     model_name_str=self._config.claude_model_name,
        #     # TODO: Finish this system prompt
        #     system_prompt="You are the Data Aggregation Specialist. Combine all CSV files in the data/ directory <METHOD_NAME_HERE>"
        # )

        # self._notification_agent: SpecializedAgent = SpecializedAgent(
        #     name_str="Visual_Construction_Agent",
        #     client=self._client,
        #     model_name_str=self._config.claude_model_name,
        #     # TODO: Finish this system prompt
        #     system_prompt="You are the Visual Construction Specialist. Create a visual for the data provided using the <METHOD_NAME_HERE>"
        # )

        self._logger = AppLogger.get_logger(self.__class__.__name__)

    async def run_workflow_async(self, user_request: str) -> None:
        self._logger.info("Resolving server application capability schemas via Event Loop...")

        # Pre-resolve the tools asynchronously using the public interface safely
        download_historical_stock_schema_dict: dict = await self._resolve_tool_schema(
            tool_name="download_historical_stock_data")
        # data_aggregation_schema:dict = await self._resolve_tool_schema(tool_name="")
        # notify_schema:dict = await self._resolve_tool_schema(tool_name="")

        self._logger.info("All tool protocol contexts successfully resolved. Launching pipeline.")

        # Step 1: The Sieve Analyst (Data Extraction)
        self._logger.info("Step 1: Routing to Fetching / Download  Agent.")
        self._data_fetching_agent.execute_turn(prompt=user_request,
                                               schema_context=download_historical_stock_schema_dict)

        # # Step 2: The Checkout Specialist (Financial Transaction)
        # self._logger.info("Step 2: Routing to Purchasing Agent.")
        # purchase_directive: str = "Execute the purchase for the best ticket in the payload."
        # self._purchasing_agent.execute_turn(
        #     prompt=purchase_directive,
        #     schema_context=purchase_schema,
        #     context_data=sieved_data_context
        # )
        #
        # # Simulating the transaction receipt returned by the Purchasing Agent's tool call
        # transaction_receipt: str = "TXN-tkt_01-998877"
        #
        # # Step 3: The Communications Specialist (Network Dispatch)
        # self._logger.info("Step 3: Routing to Notification Agent.")
        # notify_directive: str = f"Send the transaction receipt to {user_email}."
        # self._notification_agent.execute_turn(
        #     prompt=notify_directive,
        #     schema_context=notify_schema,
        #     context_data=f"Transaction Receipt: {transaction_receipt}"
        # )

        self._logger.info("Pipeline complete. Workflow successfully terminated.")

    async def _resolve_tool_schema(self, tool_name: str) -> dict[str, str | dict[str, str | list[str]]]:
        internal_tool_wrapper = await self._mcp_server.mcp.get_tool(tool_name)

        if internal_tool_wrapper is None:
            raise KeyError(f"Failed to resolve execution context: Tool '{tool_name}' not registered on server.")

        mcp_contract_protocol = internal_tool_wrapper.to_mcp_tool()

        return {
            "name": mcp_contract_protocol.name,
            "description": mcp_contract_protocol.description,
            "input_schema": mcp_contract_protocol.inputSchema
        }
