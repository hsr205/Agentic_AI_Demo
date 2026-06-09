from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    claude_api_key: str = Field(..., description="Claude API key that allows programmatic access to various LLMs under the Anthropic umbrella")
    github_access_token: str = Field(..., description="Github Access Token leveraged to programmatically accessing a Github profile")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()