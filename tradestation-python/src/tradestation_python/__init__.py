try:
    from tradestation_python._version import version as __version__
except ImportError:  # pragma: no cover
    __version__ = "unknown"

from tradestation_python._client import TradeStation  # noqa: F401