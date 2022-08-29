from typing import Any, Optional, Sequence

import grpc
from grpc.aio import ClientInterceptor

from .constants import INVEST_GRPC_API
from .typedefs import ChannelArgumentType

__all__ = ("create_channel",)


def create_channel(
    *,
    target: Optional[str] = None,
    options: Optional[ChannelArgumentType] = None,
    force_async: bool = False,
    compression: Optional[grpc.Compression] = None,
    interceptors: Optional[Sequence[ClientInterceptor]] = None,
) -> Any:
    creds = grpc.ssl_channel_credentials()
    target = target or INVEST_GRPC_API
    args = (target, creds, options, compression)
    if force_async:
        return grpc.aio.secure_channel(*args, interceptors)
    return grpc.secure_channel(*args)
