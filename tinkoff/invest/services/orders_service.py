import abc
from typing import Optional

from tinkoff.invest._errors import handle_request_error
from tinkoff.invest._grpc_helpers import (
    StorageService,
    dataclass_to_protobuff,
    protobuf_to_dataclass,
)
from tinkoff.invest.grpc import orders_pb2, orders_pb2_grpc
from tinkoff.invest.logging import get_tracking_id_from_call, log_request
from tinkoff.invest.schemas import (
    CancelOrderRequest,
    CancelOrderResponse,
    GetOrdersRequest,
    GetOrdersResponse,
    GetOrderStateRequest,
    OrderDirection,
    OrderState,
    OrderType,
    PostOrderRequest,
    PostOrderResponse,
    Quotation,
)


class IOrderService(abc.ABC):
    @abc.abstractmethod
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
        ...

    @abc.abstractmethod
    def cancel_order(
        self, *, account_id: str = "", order_id: str = ""
    ) -> CancelOrderResponse:
        ...

    @abc.abstractmethod
    def get_order_state(
        self, *, account_id: str = "", order_id: str = ""
    ) -> OrderState:
        ...

    @abc.abstractmethod
    def get_orders(self, *, account_id: str = "") -> GetOrdersResponse:
        ...


class OrdersService(StorageService[str, OrderState], IOrderService):
    _stub_factory = orders_pb2_grpc.OrdersServiceStub

    @handle_request_error("PostOrder")
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
        request = PostOrderRequest()
        request.figi = figi
        request.quantity = quantity
        if price is not None:
            request.price = price
        request.direction = direction
        request.account_id = account_id
        request.order_type = order_type
        request.order_id = order_id
        response, call = self.stub.PostOrder.with_call(
            request=dataclass_to_protobuff(request, orders_pb2.PostOrderRequest()),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "PostOrder")
        order_state = self.get_order_state(account_id=account_id, order_id=order_id)
        self._storage.add(order_state)
        return protobuf_to_dataclass(response, PostOrderResponse)

    @handle_request_error("CancelOrder")
    def cancel_order(
        self, *, account_id: str = "", order_id: str = ""
    ) -> CancelOrderResponse:
        request = CancelOrderRequest()
        request.account_id = account_id
        request.order_id = order_id
        response, call = self.stub.CancelOrder.with_call(
            request=dataclass_to_protobuff(request, orders_pb2.CancelOrderRequest()),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "CancelOrder")
        self._storage.delete(order_id)
        return protobuf_to_dataclass(response, CancelOrderResponse)

    @handle_request_error("GetOrderState")
    def get_order_state(
        self, *, account_id: str = "", order_id: str = ""
    ) -> OrderState:
        request = GetOrderStateRequest()
        request.account_id = account_id
        request.order_id = order_id
        response, call = self.stub.GetOrderState.with_call(
            request=dataclass_to_protobuff(request, orders_pb2.GetOrderStateRequest()),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetOrderState")
        order_state = self.get_order_state(account_id=account_id, order_id=order_id)
        self._storage.update(order_state.order_id, order_state)
        return protobuf_to_dataclass(response, OrderState)

    @handle_request_error("GetOrders")
    def get_orders(self, *, account_id: str = "") -> GetOrdersResponse:
        request = GetOrdersRequest()
        request.account_id = account_id
        response, call = self.stub.GetOrders.with_call(
            request=dataclass_to_protobuff(request, orders_pb2.GetOrdersRequest()),
            metadata=self.metadata,
        )
        log_request(get_tracking_id_from_call(call), "GetOrders")
        orders_response: GetOrdersResponse = protobuf_to_dataclass(
            response, GetOrdersResponse
        )
        for order_state in orders_response.orders:
            self._storage.update(order_state.order_id, order_state)
        return orders_response
