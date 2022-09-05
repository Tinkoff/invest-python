import logging
import os
from datetime import timedelta

from tinkoff.invest import CandleInterval
from tinkoff.invest.retrying.settings import RetryClientSettings
from tinkoff.invest.retrying.sync.client import RetryingClient
from tinkoff.invest.utils import now

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)

TOKEN = os.environ["INVEST_TOKEN"]

retry_settings = RetryClientSettings(use_retry=True, max_retry_attempt=2)

with RetryingClient(TOKEN, settings=retry_settings) as client:
    for candle in client.get_all_candles(
        figi="BBG000B9XRY4",
        from_=now() - timedelta(days=301),
        interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
    ):
        print(candle)
