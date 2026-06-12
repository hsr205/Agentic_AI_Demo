# TODO: (1) Finish Data Visualization Agent using Plotly
import asyncio

from agent.agent_orchestrator import AgentOrchestrator


def main() -> int:
    user_prompt: str = (
        """
        Find data for Apple and Google class A stock with a start date of January 1, 2025 to December 31, 2025.
        Then save the data to a single CSV file on my local machine at the directory: data/
        """
    )

    app_orchestrator: AgentOrchestrator = AgentOrchestrator()

    asyncio.run(app_orchestrator.run_workflow_async(user_request=user_prompt))

    return 0


if __name__ == "__main__":
    main()
