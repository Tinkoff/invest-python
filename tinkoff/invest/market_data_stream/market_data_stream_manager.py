import queue
import threading
from typing import Iterable, Iterator, TypeVar

from tinkoff.invest.market_data_stream.market_data_stream_interface import (
    IMarketDataStreamManager,
)
from tinkoff.invest.market_data_stream.stream_managers import (
    CandlesStreamManager,
    InfoStreamManager,
    LastPriceStreamManager,
    OrderBookStreamManager,
    TradesStreamManager,
)
from tinkoff.invest.schemas import MarketDataRequest, MarketDataResponse

TMarketDataStreamManager = TypeVar("TMarketDataStreamManager")
TInstrument = TypeVar("TInstrument")


class MarketDataStreamManager(IMarketDataStreamManager):
    def __init__(
        self, market_data_stream_service: "MarketDataStreamService"  # noqa: F821
    ):
        self._market_data_stream_service = market_data_stream_service
        self._market_data_stream: Iterator[MarketDataResponse]
        self._requests: queue.Queue[MarketDataRequest] = queue.Queue()
        self._unsubscribe_event = threading.Event()

    def _get_request_generator(self) -> Iterable[MarketDataRequest]:
        while not self._unsubscribe_event.is_set() or not self._requests.empty():
            if request := self._requests.get(timeout=1.0):
                yield request

    @property
    def candles(self) -> "CandlesStreamManager[MarketDataStreamManager]":
        return CandlesStreamManager[MarketDataStreamManager](parent_manager=self)

    @property
    def order_book(self) -> "OrderBookStreamManager[MarketDataStreamManager]":
        return OrderBookStreamManager[MarketDataStreamManager](parent_manager=self)

    @property
    def trades(self) -> "TradesStreamManager[MarketDataStreamManager]":
        return TradesStreamManager[MarketDataStreamManager](parent_manager=self)

    @property
    def info(self) -> "InfoStreamManager[MarketDataStreamManager]":
        return InfoStreamManager[MarketDataStreamManager](parent_manager=self)

    @property
    def last_price(self) -> "LastPriceStreamManager[MarketDataStreamManager]":
        return LastPriceStreamManager[MarketDataStreamManager](parent_manager=self)

    def subscribe(self, market_data_request: MarketDataRequest) -> None:
        self._requests.put(market_data_request)

    def unsubscribe(self, market_data_request: MarketDataRequest) -> None:
        self._requests.put(market_data_request)

    def stop(self) -> None:
        self._unsubscribe_event.set()

    def __iter__(self) -> "MarketDataStreamManager":
        self._unsubscribe_event.clear()
        self._market_data_stream = iter(
            self._market_data_stream_service.market_data_stream(
                self._get_request_generator()
            )
        )
        return self

    def __next__(self) -> MarketDataResponse:
        return next(self._market_data_stream)
