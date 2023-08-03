import abc
from datetime import datetime
from typing import Generator, Optional


class ICandleGetter(abc.ABC):
    @abc.abstractmethod
    def get_all_candles(
        self,
        *,
        from_: datetime,
        to: Optional[datetime],
        interval: "CandleInterval",  # noqa: F821 Undefined name `CandleInterval`
        figi: str,
    ) -> Generator[
        "HistoricCandle", None, None  # noqa: F821 Undefined name `HistoricCandle`
    ]:
        pass
