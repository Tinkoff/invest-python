import time

from cachetools import TTLCache as TTLCacheBase


class TTLCache(TTLCacheBase):
    def __init__(self, maxsize, ttl, timer=None, getsizeof=None):
        if timer is None:
            timer = time.monotonic
        super().__init__(maxsize=maxsize, ttl=ttl, timer=timer, getsizeof=getsizeof)
