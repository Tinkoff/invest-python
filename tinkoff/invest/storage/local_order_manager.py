import logging
from typing import Iterable

from tinkoff.invest import OrderState, Client
from tinkoff.invest.storage.order_manager import IOrderManager
from tinkoff.invest.storage.order_storage import IOrderStorage


logger = logging.getLogger(__name__)


class OrderManager(IOrderManager):
    def __init__(self, storage: IOrderStorage, client: Client):
        self._storage = storage
        self._client = client

    def cancel_order(self, order_id: str) -> None:
        with self._client as client:
            client.orders
        self._storage.delete(order_id)

        logger.info('Order %s order was cancelled', order_id)

    def get_orders(self) -> Iterable[OrderState]:
        yield from self._storage.get_all()
