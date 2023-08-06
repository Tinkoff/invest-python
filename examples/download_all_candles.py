import logging
import os
from datetime import timedelta
from pathlib import Path

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.caching.market_data_cache.cache import MarketDataCache
from tinkoff.invest.caching.market_data_cache.cache_settings import (
    MarketDataCacheSettings,
)
from tinkoff.invest.utils import now

TOKEN = os.environ["INVEST_TOKEN"]
logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)


def main():
    with Client(TOKEN) as client:
        settings = MarketDataCacheSettings(base_cache_dir=Path("market_data_cache"))
        market_data_cache = MarketDataCache(settings=settings, services=client)
        for candle in market_data_cache.get_all_candles(
            figi="BBG004730N88",
            from_=now() - timedelta(days=3),
            interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        ):
            print(candle.time)

    return 0


if __name__ == "__main__":
    main()
