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


class OrderNotFoundError(RequestError):
    def __init__(self, order_id: str):
        super().__init__(
            StatusCode.NOT_FOUND, f"Order id={order_id} was not found", metadata=None
        )


class AioRequestError(InvestError):
    def __init__(  # pylint:disable=super-init-not-called
        self, code: StatusCode, details: str, metadata: Any
    ) -> None:
        self.code = code
        self.details = details
        self.metadata = metadata
