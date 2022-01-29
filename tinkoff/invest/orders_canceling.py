from tinkoff.invest.models import AccountId
from tinkoff.invest.services import OrdersService, Services, StopOrdersService


def cancel_all_orders(services: Services, account_id: AccountId) -> None:
    orders_service: OrdersService = services.orders
    stop_orders_service: StopOrdersService = services.stop_orders

    orders_response = orders_service.get_orders(account_id=account_id)
    for order in orders_response.orders:
        orders_service.cancel_order(account_id=account_id, order_id=order.order_id)

    stop_orders_response = stop_orders_service.get_stop_orders(account_id=account_id)
    for stop_order in stop_orders_response.stop_orders:
        stop_orders_service.cancel_stop_order(
            account_id=account_id, stop_order_id=stop_order.stop_order_id
        )
