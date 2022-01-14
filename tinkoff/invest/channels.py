from typing import Literal, Union, overload

import grpc

from .constants import INVEST_GRPC_API


@overload
def create_channel(*, force_async: Literal[True]) -> grpc.aio.Channel:
    ...


@overload
def create_channel(*, force_async: Literal[False] = ...) -> grpc.Channel:
    ...


@overload
def create_channel(*, force_async: bool) -> Union[grpc.Channel, grpc.aio.Channel]:
    ...


def create_channel(
    *, force_async: bool = False
) -> Union[grpc.Channel, grpc.aio.Channel]:
    creds = grpc.ssl_channel_credentials()
    args = (INVEST_GRPC_API, creds)
    if force_async:
        return grpc.aio.secure_channel(*args)
    return grpc.secure_channel(*args)
