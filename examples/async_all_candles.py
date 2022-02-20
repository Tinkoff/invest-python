import asyncio
import os
from datetime import datetime, timedelta

from tinkoff.invest import AsyncClient, CandleInterval

TOKEN = os.environ["INVEST_TOKEN"]


async def main():
    async with AsyncClient(TOKEN) as client:
        async for candle in client.get_all_candles(
            figi="BBG004730N88",
            from_=datetime.utcnow() - timedelta(days=365),
            to=datetime.utcnow() - timedelta(days=364),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            print(candle)


if __name__ == "__main__":
    asyncio.run(main())
