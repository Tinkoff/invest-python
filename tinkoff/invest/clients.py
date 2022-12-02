from typing import List, Optional

import grpc
from grpc.aio import ClientInterceptor

from .async_services import AsyncServices
from .channels import create_channel
from .interceptors.metadata_adder_interceptor import metadata_adder_interceptor
from .metadata import get_metadata
from .services import Services
from .typedefs import ChannelArgumentType

__all__ = ("Client", "AsyncClient")


class Client:
    """
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
        self._token = token
        self._sandbox_token = sandbox_token
        self._options = options
        self._app_name = app_name
        self._metadata = get_metadata(token, app_name)

        self._channel = create_channel(target=target, options=options)
        if interceptors is None:
            interceptors = []
        self._add_metadata_interceptor(interceptors)
        self._add_logging_interceptor(interceptors)
        for interceptor in interceptors:
            self._channel = grpc.intercept_channel(self._channel, interceptor)

    def _add_metadata_interceptor(self, interceptors):
        interceptors.append(metadata_adder_interceptor(self._metadata))

    def __enter__(self) -> Services:
        channel = self._channel.__enter__()
        return Services(
            channel,
            token=self._token,
            sandbox_token=self._sandbox_token,
            app_name=self._app_name,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._channel.__exit__(exc_type, exc_val, exc_tb)
        return False

    def _add_logging_interceptor(self, interceptors):
        log_request(get_tracking_id_from_call(call), "GetAccounts")


class AsyncClient:
    """
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
        self._token = token
        self._sandbox_token = sandbox_token
        self._options = options
        self._app_name = app_name
        self._channel = create_channel(
            target=target, force_async=True, options=options, interceptors=interceptors
        )

    async def __aenter__(self) -> AsyncServices:
        channel = await self._channel.__aenter__()
        return AsyncServices(
            channel,
            token=self._token,
            sandbox_token=self._sandbox_token,
            app_name=self._app_name,
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._channel.__aexit__(exc_type, exc_val, exc_tb)
        return False
