import os
import time

from tinkoff.invest import (
    CandleInstrument,
    Client,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)

TOKEN = os.environ["INVEST_TOKEN"]


def main():
    def request_iterator():
        yield MarketDataRequest(
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
        while True:
            time.sleep(1)

    with Client(TOKEN) as client:
        for marketdata in client.market_data_stream.market_data_stream(
            request_iterator()
        ):
            print(marketdata)


if __name__ == "__main__":
    main()
