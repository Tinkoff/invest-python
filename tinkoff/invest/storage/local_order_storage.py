from typing import List, Iterable

from tinkoff.invest import OrderState
from tinkoff.invest.storage.order_storage import IOrderStorage


class OrderStorage(IOrderStorage):
    def __init__(self):
        self._orders: List[OrderState] = []

    def get_all(self) -> Iterable[OrderState]:
        yield from self._orders

    def add(self, order: OrderState) -> None:
        self._orders.append(order)

    def delete(self, order_id: str) -> None:
        for i, order in enumerate(self._orders):
            if order.order_id == order_id:
                self._orders.remove(order)
                break
        else:
            raise RuntimeError(
                f"Cannot delete order_id={order_id}, order was not found in local cache"
            )
