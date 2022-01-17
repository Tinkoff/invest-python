import asyncio
import os
import sys

from tinkoff.invest import AsyncClient


async def main() -> int:
    try:
        token = os.environ["INVEST_TOKEN"]
    except KeyError:
        print("env INVEST_TOKEN not found")  # noqa:T001
        return 1
    async with AsyncClient(token) as client:
        print(await client.users.get_accounts())  # noqa:T001

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
