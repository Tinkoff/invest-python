import os

from tinkoff.invest import (
    CandleInstrument,
    Client,
    InfoInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscribeInfoRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

TOKEN = os.environ["INVEST_TOKEN"]


def main():
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
    with Client(TOKEN) as client:
        market_data_stream = client.create_market_data_stream()
        market_data_stream.subscribe(market_data_request)
        for marketdata in market_data_stream:
            print(marketdata)
            market_data_stream.subscribe(market_data_info_request)
            if marketdata.subscribe_info_response:
                market_data_stream.unsubscribe()


if __name__ == "__main__":
    main()
