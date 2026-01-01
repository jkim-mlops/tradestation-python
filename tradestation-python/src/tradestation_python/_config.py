from functools import cached_property
from typing import Optional
from uuid import uuid4

from httpx import Client
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .types.responses import OpenID


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="TS_API_", extra="allow"
    )

    base_url: str = "https://sim-api.tradestation.com/v3"
    api_key: Optional[str] = None
    timeout: float = 30.0
    retries: int = 3


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="TS_AUTH_", extra="allow"
    )

    base_url: str = "https://signin.tradestation.com"
    audience: str = "https://api.tradestation.com"
    redirect_uri: str = "http://localhost:8080"
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    timeout: float = 30.0
    retries: int = 3
    state: str = Field(default=str(uuid4()))
    refresh_token: Optional[str] = None

    @computed_field
    @cached_property
    def openid(self) -> OpenID:
        with Client() as client:
            response = client.get(f"{self.base_url}/.well-known/openid-configuration")
            config = OpenID(**response.json())
            return config
