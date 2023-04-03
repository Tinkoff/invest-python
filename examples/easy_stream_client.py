import os

from tinkoff.invest import (
    CandleInstrument,
    Client,
    InfoInstrument,
    SubscriptionInterval,
)
from tinkoff.invest.services import MarketDataStreamManager

TOKEN = os.environ["INVEST_TOKEN"]


def main():
    with Client(TOKEN) as client:
        market_data_stream: MarketDataStreamManager = client.create_market_data_stream()
        market_data_stream.candles.waiting_close().subscribe(
            [
                CandleInstrument(
                    figi="BBG004730N88",
                    interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                )
            ]
        )
        for marketdata in market_data_stream:
            print(marketdata)
            market_data_stream.info.subscribe([InfoInstrument(figi="BBG004730N88")])
            if marketdata.subscribe_info_response:
                market_data_stream.stop()


if __name__ == "__main__":
    main()
