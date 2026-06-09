from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    claude_model_name: str = Field(...,
                                description="Claude Model to leverage during agentic AI agent application execution")
    claude_api_key: str = Field(..., description="Claude API key that allows programmatic access to various LLMs under the Anthropic umbrella")
    github_access_token: str = Field(..., description="Github Access Token leveraged to programmatically accessing a Github profile")

    ticketmaster_consumer_key: str = Field(..., description="TicketMaster Consumer Key for accessing the TicketMaster platform programmatically")
    ticketmaster_consumer_secret: str = Field(..., description="TicketMaster Consumer Secret for accessing the TicketMaster platform programmatically")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()