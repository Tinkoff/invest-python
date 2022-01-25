from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from tinkoff.invest.services import Services

from .async_services import AsyncServices
from .channels import create_channel

__all__ = ("Client", "AsyncClient")


@contextmanager
def Client(token: str) -> Generator[Services, None, None]:
    with create_channel() as channel:
        yield Services(channel, token)


@asynccontextmanager
async def AsyncClient(token: str) -> AsyncGenerator[AsyncServices, None]:
    async with create_channel(force_async=True) as channel:
        yield AsyncServices(channel, token)
