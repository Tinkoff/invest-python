# Breaking changes
## 0.2.0-beta60
- `MarketDataCache` moved into [tinkoff/invest/caching/market_data_cache/cache.py](tinkoff/invest/caching/market_data_cache/cache.py).
- Correct import is now `from tinkoff.invest.caching.market_data_cache.cache import MarketDataCache` (whereas previously was `from tinkoff.invest.services import MarketDataCache`).
- Import in [download_all_candles.py](examples/download_all_candles.py) was also corrected.