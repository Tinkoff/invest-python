import abc
from typing import Generic

from tinkoff.invest.schemas import MarketDataRequest

from .stream_managers import (
    CandlesStreamManager,
    InfoStreamManager,
    LastPriceStreamManager,
    OrderBookStreamManager,
    TradesStreamManager,
)
from .typevars import TMarketDataStreamManager


class IMarketDataStreamManager(abc.ABC, Generic[TMarketDataStreamManager]):
    @property
    @abc.abstractmethod
    def candles(self) -> CandlesStreamManager[TMarketDataStreamManager]:
        pass

    @property
    @abc.abstractmethod
    def order_book(self) -> OrderBookStreamManager[TMarketDataStreamManager]:
        pass

    @property
    @abc.abstractmethod
    def trades(self) -> TradesStreamManager[TMarketDataStreamManager]:
        pass

    @property
    @abc.abstractmethod
    def info(self) -> InfoStreamManager[TMarketDataStreamManager]:
        pass

    @property
    @abc.abstractmethod
    def last_price(self) -> LastPriceStreamManager[TMarketDataStreamManager]:
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
