import asyncio

from tinkoff.invest import AsyncClient
from tinkoff.invest.env_tools.token import TOKEN


async def main():
    async with AsyncClient(TOKEN) as client:
        print(await client.users.get_accounts())


if __name__ == "__main__":
    asyncio.run(main())
