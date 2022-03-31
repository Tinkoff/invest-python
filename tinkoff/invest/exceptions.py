from typing import Any

from grpc import StatusCode

__all__ = (
    "InvestError",
    "RequestError",
    "AioRequestError",
)


class InvestError(Exception):
    pass


class RequestError(InvestError):
    def __init__(  # pylint:disable=super-init-not-called
        self, code: StatusCode, details: str, metadata: Any
    ) -> None:
        self.code = code
        self.details = details
        self.metadata = metadata


class AioRequestError(InvestError):
    def __init__(  # pylint:disable=super-init-not-called
        self, code: StatusCode, details: str, metadata: Any
    ) -> None:
        self.code = code
        self.details = details
        self.metadata = metadata


class MarketDataStreamError(InvestError):
    pass


class IsNotSubscribedError(MarketDataStreamError):
    pass
