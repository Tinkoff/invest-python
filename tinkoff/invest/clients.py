from typing import Any, List, NamedTuple, Optional, Sequence, Tuple, Union

import grpc
from grpc.aio import ClientInterceptor

from .async_services import AsyncServices
from .channels import create_channel
from .services import Services
from .typedefs import ChannelArgumentType

__all__ = ("Client", "AsyncClient")


class Client:
    """Sync client.

    ```python
    import os
    from tinkoff.invest import Client

    TOKEN = os.environ["INVEST_TOKEN"]

    def main():
        with Client(TOKEN) as client:
            print(client.users.get_accounts())

    ```
    """

    def __init__(
        self,
        token: str,
        *,
        target: Optional[str] = None,
        sandbox_token: Optional[str] = None,
        options: Optional[ChannelArgumentType] = None,
        app_name: Optional[str] = None,
        interceptors: Optional[List[ClientInterceptor]] = None,
    ):
        interceptors = interceptors or []
        interceptors.append(MetadataInterceptor(token, app_name))

        self._channel = create_channel(
            target=target, options=options, interceptors=interceptors
        )

    def __enter__(self) -> Services:
        channel = self._channel.__enter__()
        return Services(channel)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._channel.__exit__(exc_type, exc_val, exc_tb)
        return False


class AsyncClient:
    """Async client.

    ```python
    import asyncio
    import os

    from tinkoff.invest import AsyncClient

    TOKEN = os.environ["INVEST_TOKEN"]


    async def main():
        async with AsyncClient(TOKEN) as client:
            print(await client.users.get_accounts())


    if __name__ == "__main__":
        asyncio.run(main())
    ```
    """

    def __init__(
        self,
        token: str,
        *,
        target: Optional[str] = None,
        sandbox_token: Optional[str] = None,
        options: Optional[ChannelArgumentType] = None,
        app_name: Optional[str] = None,
        interceptors: Optional[List[ClientInterceptor]] = None,
    ):
        interceptors = interceptors or []
        interceptors.append(MetadataInterceptor(token, app_name))

        self._channel = create_channel(
            target=target, force_async=True, options=options, interceptors=interceptors
        )

    async def __aenter__(self) -> AsyncServices:
        channel = await self._channel.__aenter__()
        return AsyncServices(channel)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._channel.__aexit__(exc_type, exc_val, exc_tb)
        return False


class MetadataInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    def __init__(self, token, app_name):
        self.metadata = [
            ("authorization", f"Bearer {token}"),
            ("x-app-name", app_name),
        ]

    def intercept_unary_unary(self, continuation, client_call_details, request):
        new_client_call_details = ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata=self.metadata,
            credentials=client_call_details.credentials,
            wait_for_ready=client_call_details.wait_for_ready,
            compression=client_call_details.compression,
        )

        return continuation(new_client_call_details, request)

    def intercept_stream_unary(
        self, continuation, client_call_details, request_iterator
    ):
        return continuation(client_call_details, request_iterator)

    def intercept_unary_stream(self, continuation, client_call_details, request):
        new_client_call_details = ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata=self.metadata,
            credentials=client_call_details.credentials,
            wait_for_ready=client_call_details.wait_for_ready,
            compression=client_call_details.compression,
        )

        return continuation(new_client_call_details, request)

    def intercept_stream_stream(
        self, continuation, client_call_details, request_iterator
    ):
        return continuation(client_call_details, request_iterator)


class _ClientCallDetailsFields(NamedTuple):
    method: str
    timeout: Optional[float]
    metadata: Optional[Sequence[Tuple[str, Union[str, bytes]]]]
    credentials: Optional[grpc.CallCredentials]
    wait_for_ready: Optional[bool]
    compression: Any


class ClientCallDetails(_ClientCallDetailsFields, grpc.ClientCallDetails):
    pass
