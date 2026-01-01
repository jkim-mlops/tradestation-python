from enum import Enum


class Scope(Enum):
    MARKET_DATA = "MarketData"
    READ_ACCOUNT = "ReadAccount"
    TRADE = "Trade"
    OPTION_SPREADS = "OptionSpreads"
    MATRIX = "Matrix"
    OPENID = "openid"
    OFFLINE_ACCESS = "offline_access"
    PROFILE = "profile"
    EMAIL = "email"
