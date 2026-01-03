from functools import cached_property
from typing import Any, Optional

from httpx import Auth

from ._auth import TradeStationAuth
from ._base_client import AsyncAPIClient, SyncAPIClient
from ._config import APISettings
from .resources import Brokerage, MarketData, OrderExecution


class TradeStation(SyncAPIClient):
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        auth: Optional[Auth] = None,
        timeout: Optional[float] = None,
        retries: Optional[int] = None,
    ) -> None:
        settings = APISettings()
        if base_url is None:
            base_url = settings.base_url
        if api_key is None:
            api_key = settings.api_key
        if auth is None:
            auth = TradeStationAuth()
        if timeout is None:
            timeout = settings.timeout
        if retries is None:
            retries = settings.retries

        super().__init__(
            base_url=base_url,
            api_key=api_key,
            auth=auth,
            timeout=timeout,
            retries=retries,
        )
        self._tradestation_auth = auth

    @cached_property
    def brokerage(self) -> Brokerage:
        return Brokerage(self)

    @cached_property
    def market_data(self) -> MarketData:
        return MarketData(self)

    @cached_property
    def order_execution(self) -> OrderExecution:
        return OrderExecution(self)

    @property
    def tradestation_auth(self) -> TradeStationAuth:
        """Return the TradeStationAuth instance."""
        if not isinstance(self._tradestation_auth, TradeStationAuth):
            raise TypeError("Auth must be an instance of TradeStationAuth")
        return self._tradestation_auth


class AsyncTradeStation(AsyncAPIClient):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__(*args, **kwargs)
