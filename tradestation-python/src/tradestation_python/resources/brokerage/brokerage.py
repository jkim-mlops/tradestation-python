from typing import TYPE_CHECKING

from ..._resource import SyncAPIResource
from ...types.responses import AccountsResponse

if TYPE_CHECKING:
    from tradestation._client import TradeStation


class Brokerage(SyncAPIResource):
    def __init__(self, client: "TradeStation") -> None:
        super().__init__(client)

    def accounts(self) -> AccountsResponse:
        return self._client._make_request(
            "GET", "brokerage/accounts", response_model=AccountsResponse
        )
