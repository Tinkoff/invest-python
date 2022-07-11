import dataclasses
from datetime import timedelta


@dataclasses.dataclass()
class InstrumentsCacheSettings:
    ttl: timedelta = timedelta(days=1)
