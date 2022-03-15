import asyncio
import os

from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    InfoInstrument,
    SubscriptionInterval,
)
from tinkoff.invest.async_services import AsyncMarketDataStreamManager

TOKEN = os.environ["INVEST_TOKEN"]


async def main():
    async with AsyncClient(TOKEN) as client:
        market_data_stream: AsyncMarketDataStreamManager = client.create_market_data_stream()
        await market_data_stream.candles.subscribe([
                CandleInstrument(
                    figi="BBG004730N88",
                    interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                )
            ])
        async for marketdata in market_data_stream:
            print(marketdata)
            await market_data_stream.info.subscribe([InfoInstrument(figi="BBG004730N88")])
            if marketdata.subscribe_info_response:
                market_data_stream.unsubscribe()


if __name__ == "__main__":
    asyncio.run(main())
