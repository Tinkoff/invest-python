import sys
from datetime import datetime, timedelta

from tinkoff.invest import CandleInterval, Client, get_all_candles
from tinkoff.invest.token import TOKEN


def main() -> int:
    with Client(TOKEN) as client:
        for candle in get_all_candles(
            client.market_data,
            figi="BBG004730N88",
            from_=datetime.utcnow() - timedelta(days=365),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            print(candle)

    return 0


if __name__ == "__main__":
    sys.exit(main())
