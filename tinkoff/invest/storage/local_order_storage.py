from typing import Dict, Iterable

from tinkoff.invest.schemas import OrderState
from tinkoff.invest.storage.order_storage import IOrdersStorage


class OrdersStorage(IOrdersStorage):
    def __init__(self):
        self._orders: Dict[str, OrderState] = {}

    def get_all(self) -> Iterable[OrderState]:
        yield from self._orders

    def update(self, item_id: str, new_item: OrderState) -> None:
        if item_id in self._orders:
            self._orders[item_id] = new_item
        else:
            raise KeyError(f"Cannot update order_id={item_id}, order is not in storage")

    def add(self, order: OrderState) -> None:
        if order.order_id not in self._orders:
            self._orders[order.order_id] = order
        else:
            raise KeyError(
                f"Cannot add order_id={order.order_id}, order is already in storage"
            )

    def delete(self, order_id: str) -> None:
        if order_id in self._orders:
            del self._orders[order_id]
        else:
            raise KeyError(
                f"Cannot delete order_id={order_id}, order is not in storage"
            )
