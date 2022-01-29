import asyncio

from tinkoff.invest.async_services import (
    AsyncServices,
    OrdersService,
    StopOrdersService,
)
from tinkoff.invest.models import AccountId


async def cancel_all_orders(
    async_services: AsyncServices, account_id: AccountId
) -> None:
    orders_service: OrdersService = async_services.orders
    stop_orders_service: StopOrdersService = async_services.stop_orders

    orders_response = await orders_service.get_orders(account_id=account_id)
    await asyncio.gather(
        *[
            orders_service.cancel_order(account_id=account_id, order_id=order.order_id)
            for order in orders_response.orders
        ]
    )

    stop_orders_response = await stop_orders_service.get_stop_orders(
        account_id=account_id
    )
    await asyncio.gather(
        *[
            stop_orders_service.cancel_stop_order(
                account_id=account_id, stop_order_id=stop_order.stop_order_id
            )
            for stop_order in stop_orders_response.stop_orders
        ]
    )
