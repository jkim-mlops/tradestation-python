from abc import ABC
from types import TracebackType
from typing import Any, Dict, List, Optional, Type, TypeVar

import httpx
from pydantic import BaseModel

from .types.enums import Scope

ResponseModel = TypeVar("ResponseModel", bound=BaseModel)


class BaseAuthClient(ABC):
    """Abstract base class for Auth clients."""

    def __init__(
        self,
        base_url: str,
        audience: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        response_type: str,
        state: str,
        scopes: List[Scope],
        timeout: float = 30.0,
        retries: int = 3,
    ) -> None:
        self.base_url = base_url
        self.audience = audience
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.state = state
        self.scopes = scopes
        self.timeout = timeout
        self.retries = retries


class SyncAuthClient(BaseAuthClient):
    """Synchronous HTTP Auth client."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(*args, **kwargs)
        self.client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

    def _make_request(
        self,
        method: str,
        url: str,
        response_model: Type[ResponseModel],
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ResponseModel:
        """Make HTTP request with automatic Pydantic validation."""
        request_kwargs = {}
        if params:
            request_kwargs["params"] = params
        if json:
            request_kwargs["json"] = json
        if data:
            request_kwargs["data"] = data
        if headers:
            request_kwargs["headers"] = headers

        response = self.client.request(method, url, follow_redirects=True, **request_kwargs)
        response.raise_for_status()

        return response_model.model_validate(response.json())

    def __enter__(self) -> "SyncAuthClient":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.client.close()


class BaseAPIClient(ABC):
    """Abstract base class for API clients."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        auth: Optional[httpx.Auth] = None,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries

        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

        self.auth = auth


class SyncAPIClient(BaseAPIClient):
    """Synchronous HTTP API client."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(*args, **kwargs)
        self.client = httpx.Client(
            base_url=self.base_url, headers=self.headers, auth=self.auth, timeout=self.timeout
        )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        response_model: Type[ResponseModel],
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> ResponseModel:
        """Make HTTP request with automatic Pydantic validation."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        request_kwargs = {}
        if params:
            request_kwargs["params"] = params
        if json:
            request_kwargs["json"] = json
        if data:
            request_kwargs["data"] = data
        if headers:
            request_kwargs["headers"] = headers

        response = self.client.request(method, url, **request_kwargs)
        response.raise_for_status()

        return response_model.model_validate(response.json())

    def __enter__(self) -> "SyncAPIClient":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.client.close()


class AsyncAPIClient(BaseAPIClient):
    """Asynchronous HTTP API client."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(*args, **kwargs)
        self.client = httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers, timeout=self.timeout
        )

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        response_model: type[BaseModel],
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> BaseModel:
        """Make async HTTP request with automatic Pydantic validation."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        request_kwargs = {}
        if params:
            request_kwargs["params"] = params
        if json:
            request_kwargs["json"] = json
        if data:
            request_kwargs["data"] = data
        if headers:
            request_kwargs["headers"] = headers

        response = await self.client.request(method, url, **request_kwargs)
        response.raise_for_status()

        return response_model.model_validate(response.json())

    async def __aenter__(self) -> "AsyncAPIClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.client.aclose()
