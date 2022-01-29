import asyncio
import sys

from tinkoff.invest import AsyncClient
from tinkoff.invest.token import TOKEN


async def main() -> int:
    async with AsyncClient(TOKEN) as client:
        print(await client.users.get_accounts())

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
