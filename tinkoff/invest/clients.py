from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator, Optional

from .async_services import AsyncServices
from .channels import create_channel
from .services import Services
from .typedefs import ChannelArgumentType

__all__ = ("Client", "AsyncClient")


@contextmanager
def Client(
    token: str,
    *,
    sandbox_token: Optional[str] = None,
    options: Optional[ChannelArgumentType] = None
) -> Generator[Services, None, None]:
    with create_channel(options=options) as channel:
        yield Services(channel, token=token, sandbox_token=sandbox_token)


@asynccontextmanager
async def AsyncClient(
    token: str,
    *,
    sandbox_token: Optional[str] = None,
    options: Optional[ChannelArgumentType] = None
) -> AsyncGenerator[AsyncServices, None]:
    async with create_channel(force_async=True, options=options) as channel:
        yield AsyncServices(channel, token=token, sandbox_token=sandbox_token)
