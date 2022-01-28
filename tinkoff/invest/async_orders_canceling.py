import asyncio

from tinkoff.invest.async_services import OrdersService, StopOrdersService
from tinkoff.invest.models import AccountId


class AsyncOrdersCanceler:
    def __init__(
        self,
        orders_service: OrdersService,
        stop_orders_service: StopOrdersService,
        account_id: AccountId = "",
    ):
        self._orders_service = orders_service
        self._stop_orders_service = stop_orders_service
        self._account_id = account_id

    def cancel_all(self) -> None:
        orders_response = await self._orders_service.get_orders(account_id=self._account_id)
        await asyncio.gather(
            [
                self._orders_service.cancel_order(
                    account_id=self._account_id, order_id=order.order_id
                ) for order in orders_response.orders
            ]
        )

        stop_orders_response = await self._stop_orders_service.get_stop_orders(
            account_id=self._account_id
        )
        await asyncio.gather(
            [
                self._stop_orders_service.cancel_stop_order(
                    account_id=self._account_id, stop_order_id=stop_order.stop_order_id
                ) for stop_order in stop_orders_response.stop_orders
            ]
        )
