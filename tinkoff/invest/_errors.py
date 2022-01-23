from functools import wraps
from typing import Any, Callable, TypeVar, cast

from grpc import Call, RpcError
from grpc.aio import AioRpcError

from .exceptions import AioRequestError, RequestError
from .logging import get_metadata_from_aio_error, get_metadata_from_call, log_error

TFunc = TypeVar("TFunc", bound=Callable[..., Any])


def handle_request_error(name: str):
    def decorator(func: TFunc) -> TFunc:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except RpcError as e:
                if issubclass(type(e), Call):
                    metadata = get_metadata_from_call(e)
                    tracking_id = metadata.tracking_id if metadata else None
                    log_error(
                        tracking_id,
                        name,
                        f"{e.code().name} {e.details()}",  # type:ignore
                    )
                    raise RequestError(
                        e.code(), e.details(), metadata  # type:ignore
                    ) from e
                raise

        return cast("TFunc", wrapper)

    return decorator


def handle_request_error_gen(name: str):
    def decorator(func: TFunc) -> TFunc:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                yield from func(*args, **kwargs)
            except RpcError as e:
                if issubclass(type(e), Call):
                    metadata = get_metadata_from_call(e)
                    tracking_id = metadata.tracking_id if metadata else None
                    log_error(
                        tracking_id,
                        name,
                        f"{e.code().name} {e.details()}",  # type:ignore
                    )
                    raise RequestError(
                        e.code(), e.details(), metadata  # type:ignore
                    ) from e
                raise

        return cast(TFunc, wrapper)

    return decorator


def handle_aio_request_error(name: str):
    def decorator(func: TFunc) -> TFunc:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except AioRpcError as e:
                metadata = get_metadata_from_aio_error(e)
                tracking_id = metadata.tracking_id if metadata else None
                log_error(
                    tracking_id,
                    name,
                    f"{e.code().name} {e.details()}",  # type:ignore
                )
                raise AioRequestError(
                    e.code(), e.details(), metadata  # type:ignore
                ) from e

        return cast(TFunc, wrapper)

    return decorator


def handle_aio_request_error_gen(name: str):
    def decorator(func: TFunc) -> TFunc:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                async for result in func(*args, **kwargs):
                    yield result
            except AioRpcError as e:
                metadata = get_metadata_from_aio_error(e)
                tracking_id = metadata.tracking_id if metadata else None
                log_error(
                    tracking_id,
                    name,
                    f"{e.code().name} {e.details()}",  # type:ignore
                )
                raise AioRequestError(
                    e.code(), e.details(), metadata  # type:ignore
                ) from e

        return cast(TFunc, wrapper)

    return decorator
