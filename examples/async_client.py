import asyncio
import os

from tinkoff.invest import AsyncClient

TOKEN = os.environ["INVEST_TOKEN"]


async def main():
    async with AsyncClient(TOKEN) as client:
        print(await client.users.get_accounts())


if __name__ == "__main__":
    asyncio.run(main())
