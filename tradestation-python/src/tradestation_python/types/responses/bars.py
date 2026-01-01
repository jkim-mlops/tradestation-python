from datetime import datetime
from typing import List

from pydantic import Field

from .base import BaseResponse


class Bar(BaseResponse):
    """Individual bar data model."""

    high: float = Field(alias="High")
    low: float = Field(alias="Low")
    open: float = Field(alias="Open")
    close: float = Field(alias="Close")
    timestamp: datetime = Field(alias="TimeStamp")
    total_volume: int = Field(alias="TotalVolume")
    down_ticks: int = Field(alias="DownTicks")
    down_volume: int = Field(alias="DownVolume")
    open_interest: int = Field(alias="OpenInterest")
    is_realtime: bool = Field(alias="IsRealtime")
    is_end_of_history: bool = Field(alias="IsEndOfHistory")
    total_ticks: int = Field(alias="TotalTicks")
    unchanged_ticks: int = Field(alias="UnchangedTicks")
    unchanged_volume: int = Field(alias="UnchangedVolume")
    up_ticks: int = Field(alias="UpTicks")
    up_volume: int = Field(alias="UpVolume")
    epoch: int = Field(alias="Epoch")
    bar_status: str = Field(alias="BarStatus")


class BarsResponse(BaseResponse):
    """Bars response model containing a list of bar data."""

    bars: List[Bar] = Field(alias="Bars")
