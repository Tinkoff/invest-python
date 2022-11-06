from datetime import timedelta

from cachetools import TTLCache as StandardTTLCache
from pytest_freezegun import freeze_time

from tinkoff.invest.caching.overrides import TTLCache as OverridenTTLCache


class TestTTLCache:
    def _assert_ttl_cache(self, ttl_cache_class, expires):
        with freeze_time() as frozen_datetime:
            ttl = ttl_cache_class(
                maxsize=10,
                ttl=1,
            )
            ttl.update({"1": 1})

            assert ttl.keys()
            frozen_datetime.tick(timedelta(seconds=10000))
            assert not ttl.keys() == expires

    def test_overriden_cache(self):
        self._assert_ttl_cache(OverridenTTLCache, expires=True)

    def test_standard_cache(self):
        self._assert_ttl_cache(StandardTTLCache, expires=False)
