import abc
from typing import Iterable

from tinkoff.invest import OrderState


class IOrderManager(abc.ABC):
    @abc.abstractmethod
    def get_orders(self) -> Iterable[OrderState]: ...

    @abc.abstractmethod
    def cancel_order(self, order_id: str) -> None: ...

