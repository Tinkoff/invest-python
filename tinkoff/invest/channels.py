from typing import Any, Optional

import grpc

from .constants import INVEST_GRPC_API
from .typedefs import ChannelArgumentType

__all__ = ("create_channel",)


def create_channel(
    *,
    target: Optional[str] = None,
    options: Optional[ChannelArgumentType] = None,
    force_async: bool = False
) -> Any:
    creds = grpc.ssl_channel_credentials()
    target = target or INVEST_GRPC_API
    args = (target, creds, options)
    if force_async:
        return grpc.aio.secure_channel(*args)
    return grpc.secure_channel(*args)
