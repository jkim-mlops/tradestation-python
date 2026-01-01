from typing import List, Optional

from pydantic import Field

from .base import BaseResponse


class AccountDetail(BaseResponse):
    """Account detail information."""

    is_stock_locate_eligible: bool = Field(alias="IsStockLocateEligible")
    enrolled_in_reg_t_program: bool = Field(alias="EnrolledInRegTProgram")
    requires_buying_power_warning: bool = Field(alias="RequiresBuyingPowerWarning")
    day_trading_qualified: bool = Field(alias="DayTradingQualified")
    option_approval_level: int = Field(alias="OptionApprovalLevel")
    pattern_day_trader: bool = Field(alias="PatternDayTrader")


class Account(BaseResponse):
    """Account information model."""

    account_id: str = Field(alias="AccountID")
    currency: str = Field(alias="Currency")
    status: str = Field(alias="Status")
    account_type: str = Field(alias="AccountType")
    account_detail: Optional[AccountDetail] = Field(None, alias="AccountDetail")


class AccountsResponse(BaseResponse):
    accounts: List[Account] = Field(alias="Accounts")
