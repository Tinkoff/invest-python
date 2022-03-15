import abc
from typing import TypeVar

from tinkoff.invest.market_data_stream.stream_managers import (
    CandlesStreamManager,
    InfoStreamManager,
    LastPriceStreamManager,
    OrderBookStreamManager,
    TradesStreamManager,
)
from tinkoff.invest.schemas import MarketDataRequest

TMarketDataStreamManager = TypeVar("TMarketDataStreamManager")
TInstrument = TypeVar("TInstrument")


class IMarketDataStreamManager(abc.ABC):
    @property
    @abc.abstractmethod
    def candles(self) -> CandlesStreamManager["IMarketDataStreamManager"]:
        pass

    @property
    @abc.abstractmethod
    def order_book(self) -> OrderBookStreamManager["IMarketDataStreamManager"]:
        pass

    @property
    @abc.abstractmethod
    def trades(self) -> TradesStreamManager["IMarketDataStreamManager"]:
        pass

    @property
    @abc.abstractmethod
    def info(self) -> InfoStreamManager["IMarketDataStreamManager"]:
        pass

    @property
    @abc.abstractmethod
    def last_price(self) -> LastPriceStreamManager["IMarketDataStreamManager"]:
        pass

    @abc.abstractmethod
    def subscribe(self, market_data_request: MarketDataRequest) -> None:
        pass

    @abc.abstractmethod
    def unsubscribe(self, market_data_request: MarketDataRequest) -> None:
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        pass
