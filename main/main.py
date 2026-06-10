from client.client_orchestrator import ClientOrchestrator


def main() -> int:
    user_prompt_criteria: str = (
        "Find upcoming events for the New York Knicks at Madison Square Garden "
        "under $50 on 2026-06-10 containing 'Watch Party' in the name."
    )

    orchestration_engine = ClientOrchestrator()
    status_exit_code: int = orchestration_engine.execute_pipeline(prompt=user_prompt_criteria)
    return status_exit_code


if __name__ == "__main__":
    main()
