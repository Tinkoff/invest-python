import asyncio
import os

from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    InfoInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscribeInfoRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

TOKEN = os.environ["INVEST_TOKEN"]


async def main():
    market_data_request = MarketDataRequest(
        subscribe_candles_request=SubscribeCandlesRequest(
            subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
            instruments=[
                CandleInstrument(
                    figi="BBG004730N88",
                    interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                )
            ],
        )
    )
    market_data_info_request = MarketDataRequest(
        subscribe_info_request=SubscribeInfoRequest(
            subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
            instruments=[InfoInstrument(figi="BBG004730N88")],
        )
    )
    async with AsyncClient(TOKEN) as client:
        market_data_stream = client.create_market_data_stream()
        await market_data_stream.subscribe(market_data_request)
        async for marketdata in market_data_stream:
            print(marketdata)
            await market_data_stream.subscribe(market_data_info_request)
            if marketdata.subscribe_info_response:
                market_data_stream.unsubscribe()


if __name__ == "__main__":
    asyncio.run(main())
