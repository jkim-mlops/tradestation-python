from typing import TYPE_CHECKING, Optional

from ..._resource import SyncAPIResource

if TYPE_CHECKING:
    from tradestation._client import TradeStation

from datetime import datetime

from ...types.enums import SessionTemplate, Unit
from ...types.responses import BarsResponse


class MarketData(SyncAPIResource):
    def __init__(self, client: "TradeStation") -> None:
        super().__init__(client)

    def bars(
        self,
        symbol: str,
        interval: int = 1,
        unit: Unit = Unit.DAILY,
        barsback: Optional[int] = None,
        firstdate: Optional[datetime] = None,
        lastdate: Optional[datetime] = None,
        sessiontemplate: Optional[SessionTemplate] = None,
    ) -> BarsResponse:
        """
        Get bar data for a symbol.

        Args:
            symbol: The symbol to get bars for
            interval: Interval that each bar will consist of (default: 1, max: 1440 for minutes)
            unit: The unit of time for each bar interval. Valid values: Minute, Daily, Weekly, Monthly (default: Daily)
            barsback: Number of bars back to fetch (mutually exclusive with firstdate)
            firstdate: The first date as datetime object (mutually exclusive with barsback)
            lastdate: The last date as datetime object (defaults to current timestamp)
            sessiontemplate: US stock market session template.
                Valid values: USEQPre, USEQPost, USEQPreAndPost, USEQ24Hour, Default

        Returns:
            BarsResponse: The bars response containing bar data

        Note:
            Datetime parameters are automatically formatted as ISO 8601 strings (YYYY-MM-DDTHH:MM:SSZ)
            when sent to the API.
        """
        params = {
            "interval": str(interval),
            "unit": unit.value,
        }
        dt_format = r"%Y-%m-%dT%H:%M:%SZ"

        # Add optional parameters if provided
        if barsback is not None:
            params["barsback"] = str(barsback)
        if firstdate is not None:
            params["firstdate"] = firstdate.strftime(dt_format)
        if lastdate is not None:
            params["lastdate"] = lastdate.strftime(dt_format)
        if sessiontemplate is not None:
            params["sessiontemplate"] = sessiontemplate.value

        return self._client._make_request(
            "GET",
            f"marketdata/barcharts/{symbol}",
            params=params,
            response_model=BarsResponse,
        )
