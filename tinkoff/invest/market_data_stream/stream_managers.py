import abc
from typing import Generic, List, TypeVar

from tinkoff.invest.schemas import (
    CandleInstrument,
    InfoInstrument,
    LastPriceInstrument,
    MarketDataRequest,
    OrderBookInstrument,
    SubscribeCandlesRequest,
    SubscribeInfoRequest,
    SubscribeLastPriceRequest,
    SubscribeOrderBookRequest,
    SubscribeTradesRequest,
    SubscriptionAction,
    TradeInstrument,
)

TMarketDataStreamManager = TypeVar("TMarketDataStreamManager")
TInstrument = TypeVar("TInstrument")


class BaseStreamManager(abc.ABC, Generic[TInstrument, TMarketDataStreamManager]):
    def __init__(self, parent_manager: TMarketDataStreamManager):
        self._parent_manager = parent_manager

    @abc.abstractmethod
    def _get_request(
        self,
        subscription_action: SubscriptionAction,
        instruments: List[TInstrument],
    ):
        pass

    def subscribe(self, instruments: List[TInstrument]) -> TMarketDataStreamManager:
        self._parent_manager.subscribe(
            self._get_request(
                SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE, instruments
            )
        )

        return self._parent_manager

    def unsubscribe(self, instruments: List[TInstrument]) -> TMarketDataStreamManager:
        self._parent_manager.unsubscribe(
            self._get_request(
                SubscriptionAction.SUBSCRIPTION_ACTION_UNSUBSCRIBE, instruments
            )
        )

        return self._parent_manager


class CandlesStreamManager(
    BaseStreamManager[CandleInstrument, TMarketDataStreamManager]
):
    def __init__(self, parent_manager: TMarketDataStreamManager):
        super().__init__(parent_manager)
        self._parent_manager = parent_manager

    def _get_request(
        self,
        subscription_action: SubscriptionAction,
        instruments: List[CandleInstrument],
    ) -> MarketDataRequest:
        return MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                subscription_action=subscription_action,
                instruments=instruments,
            )
        )


class OrderBookStreamManager(
    BaseStreamManager[OrderBookInstrument, TMarketDataStreamManager]
):
    def __init__(self, parent_manager: TMarketDataStreamManager):
        super().__init__(parent_manager)
        self._parent_manager = parent_manager

    def _get_request(
        self,
        subscription_action: SubscriptionAction,
        instruments: List[OrderBookInstrument],
    ) -> MarketDataRequest:
        return MarketDataRequest(
            subscribe_order_book_request=SubscribeOrderBookRequest(
                subscription_action=subscription_action,
                instruments=instruments,
            )
        )


class TradesStreamManager(BaseStreamManager[TradeInstrument, TMarketDataStreamManager]):
    def __init__(self, parent_manager: TMarketDataStreamManager):
        super().__init__(parent_manager)
        self._parent_manager = parent_manager

    def _get_request(
        self,
        subscription_action: SubscriptionAction,
        instruments: List[TradeInstrument],
    ) -> MarketDataRequest:
        return MarketDataRequest(
            subscribe_trades_request=SubscribeTradesRequest(
                subscription_action=subscription_action,
                instruments=instruments,
            )
        )


class InfoStreamManager(BaseStreamManager[InfoInstrument, TMarketDataStreamManager]):
    def __init__(self, parent_manager: TMarketDataStreamManager):
        super().__init__(parent_manager)
        self._parent_manager = parent_manager

    def _get_request(
        self,
        subscription_action: SubscriptionAction,
        instruments: List[InfoInstrument],
    ) -> MarketDataRequest:
        return MarketDataRequest(
            subscribe_info_request=SubscribeInfoRequest(
                subscription_action=subscription_action,
                instruments=instruments,
            )
        )


class LastPriceStreamManager(
    BaseStreamManager[LastPriceInstrument, TMarketDataStreamManager]
):
    def __init__(self, parent_manager: TMarketDataStreamManager):
        super().__init__(parent_manager)
        self._parent_manager = parent_manager

    def _get_request(
        self,
        subscription_action: SubscriptionAction,
        instruments: List[LastPriceInstrument],
    ) -> MarketDataRequest:
        return MarketDataRequest(
            subscribe_last_price_request=SubscribeLastPriceRequest(
                subscription_action=subscription_action,
                instruments=instruments,
            )
        )
