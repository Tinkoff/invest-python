import logging
import os
from datetime import datetime, timedelta

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.caching.cache_settings import MarketDataCacheSettings
from tinkoff.invest.services import MarketDataCache
from tinkoff.invest.utils import now

TOKEN = os.environ["INVEST_TOKEN"]
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)


def main():
    with Client(TOKEN) as client:
        settings = MarketDataCacheSettings()
        market_data_cache = MarketDataCache(settings=settings, services=client)
        for candle in market_data_cache.get_all_candles(
            figi="BBG004730N88",
            from_=now() - timedelta(days=30),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            print(candle)
            pass

    return 0


if __name__ == "__main__":
    main()
