import logging
from collections import namedtuple
from contextvars import ContextVar
from typing import Any, Optional

from .constants import (
    MESSAGE,
    X_RATELIMIT_LIMIT,
    X_RATELIMIT_REMAINING,
    X_RATELIMIT_RESET,
    X_TRACKING_ID,
)

__all__ = (
    "get_current_tracking_id",
    "get_tracking_id_from_call",
    "get_tracking_id_from_coro",
    "get_metadata_from_call",
    "get_metadata_from_aio_error",
    "log_request",
    "log_error",
)

logger = logging.getLogger(__name__)

_TRACKING_ID: ContextVar[Optional[str]] = ContextVar("tracking_id", default=None)
Metadata = namedtuple(
    "Metadata",
    (
        "tracking_id",
        "ratelimit_limit",
        "ratelimit_remaining",
        "ratelimit_reset",
        "message",
    ),
)


def get_current_tracking_id() -> Optional[str]:
    return _TRACKING_ID.get() or None


def log_request(tracking_id: Optional[str], name: str) -> None:
    _TRACKING_ID.set(tracking_id)
    logger.info("%s %s", tracking_id, name)


def log_error(tracking_id: Optional[str], name: str, text: str) -> None:
    _TRACKING_ID.set(tracking_id)
    logger.error("%s %s %s", tracking_id, name, text)


def get_tracking_id_from_call(call: Any) -> Optional[str]:
    metadata = call.initial_metadata() or call.trailing_metadata()
    for item in metadata:
        if item.key == X_TRACKING_ID:
            return item.value
    return None


async def get_tracking_id_from_coro(coro: Any) -> Optional[str]:
    metadata = await coro.initial_metadata() or await coro.trailing_metadata()
    for key, value in metadata:
        if key == X_TRACKING_ID:
            return value
    return None


def get_metadata_from_call(call: Any) -> Optional[Metadata]:
    metadata = call.initial_metadata() or call.trailing_metadata()
    tracking_id = None
    ratelimit_limit = None
    ratelimit_remaining = None
    ratelimit_reset = None
    message = None
    for item in metadata:
        if item.key == X_TRACKING_ID:
            tracking_id = item.value
        elif item.key == X_RATELIMIT_LIMIT:
            ratelimit_limit = item.value
        elif item.key == X_RATELIMIT_REMAINING:
            ratelimit_remaining = int(item.value)
        elif item.key == X_RATELIMIT_RESET:
            ratelimit_reset = int(item.value)
        elif item.key == MESSAGE:
            message = item.value
    if not any(
        (tracking_id, ratelimit_limit, ratelimit_remaining, ratelimit_reset, message)
    ):
        return None
    return Metadata(
        tracking_id, ratelimit_limit, ratelimit_remaining, ratelimit_reset, message
    )


def get_metadata_from_aio_error(err: Any) -> Optional[Metadata]:
    metadata = err.initial_metadata() or err.trailing_metadata()
    tracking_id = None
    ratelimit_limit = None
    ratelimit_remaining = None
    ratelimit_reset = None
    message = None
    for key, value in metadata:
        if key == X_TRACKING_ID:
            tracking_id = value
        elif key == X_RATELIMIT_LIMIT:
            ratelimit_limit = value
        elif key == X_RATELIMIT_REMAINING:
            ratelimit_remaining = int(value)
        elif key == X_RATELIMIT_RESET:
            ratelimit_reset = int(value)
        elif key == MESSAGE:
            message = value
    if not any(
        (tracking_id, ratelimit_limit, ratelimit_remaining, ratelimit_reset, message)
    ):
        return None
    return Metadata(
        tracking_id, ratelimit_limit, ratelimit_remaining, ratelimit_reset, message
    )
