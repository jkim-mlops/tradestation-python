import time
from typing import TYPE_CHECKING

import anyio

if TYPE_CHECKING:
    from ._client import AsyncTradeStation, TradeStation


class SyncAPIResource:
    _client: "TradeStation"

    def __init__(self, client: "TradeStation") -> None:
        self._client = client

    def _sleep(self, seconds: float) -> None:
        time.sleep(seconds)


class AsyncAPIResource:
    _client: "AsyncTradeStation"

    def __init__(self, client: "AsyncTradeStation") -> None:
        self._client = client

    async def _sleep(self, seconds: float) -> None:
        await anyio.sleep(seconds)
