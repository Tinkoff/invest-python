import os
from datetime import datetime, timedelta

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now

TOKEN = os.environ["INVEST_TOKEN"]


def main():
    with Client(TOKEN) as client:
        for candle in client.get_all_candles(
            figi="BBG004730N88",
            from_=now() - timedelta(days=30),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            print(candle)

    return 0


if __name__ == "__main__":
    main()
