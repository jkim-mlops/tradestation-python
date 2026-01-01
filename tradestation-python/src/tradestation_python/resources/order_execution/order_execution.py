from typing import TYPE_CHECKING

from ..._resource import SyncAPIResource

if TYPE_CHECKING:
    from tradestation._client import TradeStation


class OrderExecution(SyncAPIResource):
    def __init__(self, client: "TradeStation") -> None:
        super().__init__(client)
