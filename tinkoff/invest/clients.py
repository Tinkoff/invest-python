from typing import Optional

from .async_services import AsyncServices
from .channels import create_channel
from .services import Services
from .typedefs import ChannelArgumentType

__all__ = ("Client", "AsyncClient")


class Client:
    def __init__(
        self,
        token: str,
        *,
        sandbox_token: Optional[str] = None,
        options: Optional[ChannelArgumentType] = None,
        app_name: Optional[str] = None,
    ):
        self._token = token
        self._sandbox_token = sandbox_token
        self._options = options
        self._app_name = app_name
        self._channel = create_channel(options=options)

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


class AsyncClient:
    def __init__(
        self,
        token: str,
        *,
        sandbox_token: Optional[str] = None,
        options: Optional[ChannelArgumentType] = None,
        app_name: Optional[str] = None,
    ):
        self._token = token
        self._sandbox_token = sandbox_token
        self._options = options
        self._app_name = app_name
        self._channel = create_channel(force_async=True, options=options)

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
