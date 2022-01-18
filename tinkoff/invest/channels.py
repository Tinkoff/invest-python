from typing import Literal, Optional, Union, overload

import grpc

from .constants import INVEST_GRPC_API

__all__ = ("create_channel",)


@overload
def create_channel(
    *, target: Optional[str] = ..., force_async: Literal[False]
) -> grpc.Channel:
    ...


@overload
def create_channel(
    *, target: Optional[str] = ..., force_async: Literal[True]
) -> grpc.aio.Channel:
    ...


@overload
def create_channel(
    *, target: Optional[str] = ..., force_async: bool = ...
) -> Union[grpc.Channel, grpc.aio.Channel]:
    ...


def create_channel(
    *, target: Optional[str] = None, force_async: bool = False
) -> Union[grpc.Channel, grpc.aio.Channel]:
    creds = grpc.ssl_channel_credentials()
    target = target or INVEST_GRPC_API
    args = (target, creds)
    if force_async:
        return grpc.aio.secure_channel(*args)
    return grpc.secure_channel(*args)
