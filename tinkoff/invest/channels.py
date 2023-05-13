import itertools
from typing import Any, Optional, Sequence

import grpc
from grpc.aio import ClientInterceptor

from .constants import INVEST_GRPC_API, MAX_RECEIVE_MESSAGE_LENGTH
from .typedefs import ChannelArgumentType

__all__ = ("create_channel",)


MAX_RECEIVE_MESSAGE_LENGTH_OPTION = "grpc.max_receive_message_length"


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
    if options is None:
        options = []

    options = _with_max_receive_message_length_option(options)

    args = (target, creds, options, compression)
    if force_async:
        return grpc.aio.secure_channel(*args, interceptors)
    return grpc.intercept_channel(grpc.secure_channel(*args), *interceptors or [])


def _with_max_receive_message_length_option(
    options: ChannelArgumentType,
) -> ChannelArgumentType:
    if not _contains_option(options, MAX_RECEIVE_MESSAGE_LENGTH_OPTION):
        option = (MAX_RECEIVE_MESSAGE_LENGTH_OPTION, MAX_RECEIVE_MESSAGE_LENGTH)
        return list(itertools.chain(options, [option]))
    return options


def _contains_option(options: ChannelArgumentType, expected_option_name: str) -> bool:
    for option_name, _ in options:
        if option_name == expected_option_name:
            return True
    return False
