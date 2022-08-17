import logging
import os
from pprint import pprint

from tinkoff.invest import Client, InstrumentIdType
from tinkoff.invest.caching.instruments_cache.instruments_cache import InstrumentsCache
from tinkoff.invest.caching.instruments_cache.settings import InstrumentsCacheSettings

TOKEN = os.environ["INVEST_TOKEN"]


logging.basicConfig(level=logging.INFO)


def main():
    with Client(TOKEN) as client:
        inst = client.instruments.etfs().instruments[-1]
        pprint(inst)

        from_server = client.instruments.etf_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID,
            class_code=inst.class_code,
            id=inst.uid,
        )
        pprint(from_server)

        settings = InstrumentsCacheSettings()
        instruments_cache = InstrumentsCache(
            settings=settings, instruments_service=client.instruments
        )

        from_cache = instruments_cache.etf_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID,
            class_code=inst.class_code,
            id=inst.uid,
        )
        pprint(from_cache)

        if str(from_server) != str(from_cache):
            raise Exception("cache miss")


if __name__ == "__main__":
    main()
