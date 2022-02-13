from datetime import datetime, timedelta

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.token import TOKEN


def main():
    with Client(TOKEN) as client:
        for candle in client.get_all_candles(
            figi="BBG004730N88",
            from_=datetime.utcnow() - timedelta(days=365),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            print(candle)

    return 0


if __name__ == "__main__":
    main()
