from typing import List, Optional

from tinkoff.invest.schemas import (
    CancelOrderResponse,
    GetOrdersResponse,
    OrderDirection,
    OrderState,
    OrderType,
    PostOrderResponse,
    Quotation,
)
from tinkoff.invest.services.orders_service import IOrdersService
from tinkoff.invest.storages.orders_storage import IOrdersStorage


class CachingOrdersService(IOrdersService):
    def __init__(self, orders_storage: IOrdersStorage, orders_service: IOrdersService):
        self._orders_storage = orders_storage
        self._orders_service = orders_service

    def post_order(
        self,
        *,
        figi: str = "",
        quantity: int = 0,
        price: Optional[Quotation] = None,
        direction: OrderDirection = OrderDirection(0),
        account_id: str = "",
        order_type: OrderType = OrderType(0),
        order_id: str = "",
    ) -> PostOrderResponse:
        response = self._orders_service.post_order(
            figi=figi,
            quantity=quantity,
            price=price,
            direction=direction,
            account_id=account_id,
            order_type=order_type,
            order_id=order_id,
        )
        order_state = self._orders_service.get_order_state(
            account_id=account_id, order_id=order_id
        )
        self._orders_storage.set(item_id=order_state.order_id, new_item=order_state)
        return response  # noqa: R504

    def cancel_order(
        self, *, account_id: str = "", order_id: str = ""
    ) -> CancelOrderResponse:
        response = self._orders_service.cancel_order(
            account_id=account_id,
            order_id=order_id,
        )
        self._orders_storage.delete(item_id=order_id)
        return response  # noqa: R504

    def get_order_state(
        self, *, account_id: str = "", order_id: str = ""
    ) -> OrderState:
        order_state = self._orders_service.get_order_state(
            account_id=account_id,
            order_id=order_id,
        )
        self._orders_storage.set(item_id=order_state.order_id, new_item=order_state)
        return order_state

    def _delete_outdated_orders(self, current_orders: List[OrderState]) -> None:
        for order_id, order_state in self._orders_storage.items():
            if order_state not in current_orders:
                self._orders_storage.delete(item_id=order_id)

    def get_orders(self, *, account_id: str = "") -> GetOrdersResponse:
        response = self._orders_service.get_orders(
            account_id=account_id,
        )
        current_orders = response.orders
        self._delete_outdated_orders(current_orders=current_orders)
        for order_state in current_orders:
            self._orders_storage.set(order_state.order_id, order_state)
        return response
