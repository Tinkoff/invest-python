import os
import sys
from datetime import datetime, timedelta

from tinkoff.invest import CandleInterval, Client, get_all_candles


def main() -> int:
    try:
        token = os.environ["INVEST_TOKEN"]
    except KeyError:
        print("env INVEST_TOKEN not found")  # noqa:T001
        return 1
    with Client(token) as client:
        for candle in get_all_candles(
            client.market_data,
            figi="BBG004730N88",
            from_=datetime.utcnow() - timedelta(days=365),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            print(candle)  # noqa:T001

    return 0


if __name__ == "__main__":
    sys.exit(main())
