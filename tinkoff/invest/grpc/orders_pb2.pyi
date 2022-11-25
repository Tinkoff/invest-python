"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import tinkoff.invest.grpc.common_pb2
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _OrderDirection:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _OrderDirectionEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_OrderDirection.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    ORDER_DIRECTION_UNSPECIFIED: _OrderDirection.ValueType  # 0
    """Значение не указано"""
    ORDER_DIRECTION_BUY: _OrderDirection.ValueType  # 1
    """Покупка"""
    ORDER_DIRECTION_SELL: _OrderDirection.ValueType  # 2
    """Продажа"""

class OrderDirection(_OrderDirection, metaclass=_OrderDirectionEnumTypeWrapper):
    """Направление операции."""

ORDER_DIRECTION_UNSPECIFIED: OrderDirection.ValueType  # 0
"""Значение не указано"""
ORDER_DIRECTION_BUY: OrderDirection.ValueType  # 1
"""Покупка"""
ORDER_DIRECTION_SELL: OrderDirection.ValueType  # 2
"""Продажа"""
global___OrderDirection = OrderDirection

class _OrderType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _OrderTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_OrderType.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    ORDER_TYPE_UNSPECIFIED: _OrderType.ValueType  # 0
    """Значение не указано"""
    ORDER_TYPE_LIMIT: _OrderType.ValueType  # 1
    """Лимитная"""
    ORDER_TYPE_MARKET: _OrderType.ValueType  # 2
    """Рыночная"""

class OrderType(_OrderType, metaclass=_OrderTypeEnumTypeWrapper):
    """Тип заявки."""

ORDER_TYPE_UNSPECIFIED: OrderType.ValueType  # 0
"""Значение не указано"""
ORDER_TYPE_LIMIT: OrderType.ValueType  # 1
"""Лимитная"""
ORDER_TYPE_MARKET: OrderType.ValueType  # 2
"""Рыночная"""
global___OrderType = OrderType

class _OrderExecutionReportStatus:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _OrderExecutionReportStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_OrderExecutionReportStatus.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    EXECUTION_REPORT_STATUS_UNSPECIFIED: _OrderExecutionReportStatus.ValueType  # 0
    EXECUTION_REPORT_STATUS_FILL: _OrderExecutionReportStatus.ValueType  # 1
    """Исполнена"""
    EXECUTION_REPORT_STATUS_REJECTED: _OrderExecutionReportStatus.ValueType  # 2
    """Отклонена"""
    EXECUTION_REPORT_STATUS_CANCELLED: _OrderExecutionReportStatus.ValueType  # 3
    """Отменена пользователем"""
    EXECUTION_REPORT_STATUS_NEW: _OrderExecutionReportStatus.ValueType  # 4
    """Новая"""
    EXECUTION_REPORT_STATUS_PARTIALLYFILL: _OrderExecutionReportStatus.ValueType  # 5
    """Частично исполнена"""

class OrderExecutionReportStatus(_OrderExecutionReportStatus, metaclass=_OrderExecutionReportStatusEnumTypeWrapper):
    """Текущий статус заявки (поручения)"""

EXECUTION_REPORT_STATUS_UNSPECIFIED: OrderExecutionReportStatus.ValueType  # 0
EXECUTION_REPORT_STATUS_FILL: OrderExecutionReportStatus.ValueType  # 1
"""Исполнена"""
EXECUTION_REPORT_STATUS_REJECTED: OrderExecutionReportStatus.ValueType  # 2
"""Отклонена"""
EXECUTION_REPORT_STATUS_CANCELLED: OrderExecutionReportStatus.ValueType  # 3
"""Отменена пользователем"""
EXECUTION_REPORT_STATUS_NEW: OrderExecutionReportStatus.ValueType  # 4
"""Новая"""
EXECUTION_REPORT_STATUS_PARTIALLYFILL: OrderExecutionReportStatus.ValueType  # 5
"""Частично исполнена"""
global___OrderExecutionReportStatus = OrderExecutionReportStatus

class _PriceType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _PriceTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_PriceType.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PRICE_TYPE_UNSPECIFIED: _PriceType.ValueType  # 0
    """Значение не определено."""
    PRICE_TYPE_POINT: _PriceType.ValueType  # 1
    """Цена в пунктах (только для фьючерсов и облигаций)."""
    PRICE_TYPE_CURRENCY: _PriceType.ValueType  # 2
    """Цена в валюте расчётов по инструменту."""

class PriceType(_PriceType, metaclass=_PriceTypeEnumTypeWrapper):
    """Тип цены."""

PRICE_TYPE_UNSPECIFIED: PriceType.ValueType  # 0
"""Значение не определено."""
PRICE_TYPE_POINT: PriceType.ValueType  # 1
"""Цена в пунктах (только для фьючерсов и облигаций)."""
PRICE_TYPE_CURRENCY: PriceType.ValueType  # 2
"""Цена в валюте расчётов по инструменту."""
global___PriceType = PriceType

class TradesStreamRequest(google.protobuf.message.Message):
    """Запрос установки соединения."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCOUNTS_FIELD_NUMBER: builtins.int
    @property
    def accounts(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Идентификаторы счетов."""
    def __init__(
        self,
        *,
        accounts: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["accounts", b"accounts"]) -> None: ...

global___TradesStreamRequest = TradesStreamRequest

class TradesStreamResponse(google.protobuf.message.Message):
    """Информация о торговых поручениях."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ORDER_TRADES_FIELD_NUMBER: builtins.int
    PING_FIELD_NUMBER: builtins.int
    @property
    def order_trades(self) -> global___OrderTrades:
        """Информация об исполнении торгового поручения."""
    @property
    def ping(self) -> tinkoff.invest.grpc.common_pb2.Ping:
        """Проверка активности стрима."""
    def __init__(
        self,
        *,
        order_trades: global___OrderTrades | None = ...,
        ping: tinkoff.invest.grpc.common_pb2.Ping | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["order_trades", b"order_trades", "payload", b"payload", "ping", b"ping"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["order_trades", b"order_trades", "payload", b"payload", "ping", b"ping"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["payload", b"payload"]) -> typing_extensions.Literal["order_trades", "ping"] | None: ...

global___TradesStreamResponse = TradesStreamResponse

class OrderTrades(google.protobuf.message.Message):
    """Информация об исполнении торгового поручения."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ORDER_ID_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    DIRECTION_FIELD_NUMBER: builtins.int
    FIGI_FIELD_NUMBER: builtins.int
    TRADES_FIELD_NUMBER: builtins.int
    ACCOUNT_ID_FIELD_NUMBER: builtins.int
    INSTRUMENT_UID_FIELD_NUMBER: builtins.int
    order_id: builtins.str
    """Идентификатор торгового поручения."""
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Дата и время создания сообщения в часовом поясе UTC."""
    direction: global___OrderDirection.ValueType
    """Направление сделки."""
    figi: builtins.str
    """Figi-идентификатор инструмента."""
    @property
    def trades(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OrderTrade]:
        """Массив сделок."""
    account_id: builtins.str
    """Идентификатор счёта."""
    instrument_uid: builtins.str
    """UID идентификатор инструмента."""
    def __init__(
        self,
        *,
        order_id: builtins.str = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        direction: global___OrderDirection.ValueType = ...,
        figi: builtins.str = ...,
        trades: collections.abc.Iterable[global___OrderTrade] | None = ...,
        account_id: builtins.str = ...,
        instrument_uid: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_at", b"created_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_id", b"account_id", "created_at", b"created_at", "direction", b"direction", "figi", b"figi", "instrument_uid", b"instrument_uid", "order_id", b"order_id", "trades", b"trades"]) -> None: ...

global___OrderTrades = OrderTrades

class OrderTrade(google.protobuf.message.Message):
    """Информация о сделке."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATE_TIME_FIELD_NUMBER: builtins.int
    PRICE_FIELD_NUMBER: builtins.int
    QUANTITY_FIELD_NUMBER: builtins.int
    TRADE_ID_FIELD_NUMBER: builtins.int
    @property
    def date_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Дата и время совершения сделки в часовом поясе UTC."""
    @property
    def price(self) -> tinkoff.invest.grpc.common_pb2.Quotation:
        """Цена за 1 инструмент, по которой совершена сделка."""
    quantity: builtins.int
    """Количество лотов в сделке."""
    trade_id: builtins.str
    """Идентификатор сделки"""
    def __init__(
        self,
        *,
        date_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        price: tinkoff.invest.grpc.common_pb2.Quotation | None = ...,
        quantity: builtins.int = ...,
        trade_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["date_time", b"date_time", "price", b"price"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["date_time", b"date_time", "price", b"price", "quantity", b"quantity", "trade_id", b"trade_id"]) -> None: ...

global___OrderTrade = OrderTrade

class PostOrderRequest(google.protobuf.message.Message):
    """Запрос выставления торгового поручения."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FIGI_FIELD_NUMBER: builtins.int
    QUANTITY_FIELD_NUMBER: builtins.int
    PRICE_FIELD_NUMBER: builtins.int
    DIRECTION_FIELD_NUMBER: builtins.int
    ACCOUNT_ID_FIELD_NUMBER: builtins.int
    ORDER_TYPE_FIELD_NUMBER: builtins.int
    ORDER_ID_FIELD_NUMBER: builtins.int
    INSTRUMENT_ID_FIELD_NUMBER: builtins.int
    figi: builtins.str
    """Figi-идентификатор инструмента."""
    quantity: builtins.int
    """Количество лотов."""
    @property
    def price(self) -> tinkoff.invest.grpc.common_pb2.Quotation:
        """Цена за 1 инструмент. Для получения стоимости лота требуется умножить на лотность инструмента. Игнорируется для рыночных поручений."""
    direction: global___OrderDirection.ValueType
    """Направление операции."""
    account_id: builtins.str
    """Номер счёта."""
    order_type: global___OrderType.ValueType
    """Тип заявки."""
    order_id: builtins.str
    """Идентификатор запроса выставления поручения для целей идемпотентности. Максимальная длина 36 символов."""
    instrument_id: builtins.str
    """Идентификатор инструмента, принимает значения Figi или Instrument_uid."""
    def __init__(
        self,
        *,
        figi: builtins.str = ...,
        quantity: builtins.int = ...,
        price: tinkoff.invest.grpc.common_pb2.Quotation | None = ...,
        direction: global___OrderDirection.ValueType = ...,
        account_id: builtins.str = ...,
        order_type: global___OrderType.ValueType = ...,
        order_id: builtins.str = ...,
        instrument_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["price", b"price"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_id", b"account_id", "direction", b"direction", "figi", b"figi", "instrument_id", b"instrument_id", "order_id", b"order_id", "order_type", b"order_type", "price", b"price", "quantity", b"quantity"]) -> None: ...

global___PostOrderRequest = PostOrderRequest

class PostOrderResponse(google.protobuf.message.Message):
    """Информация о выставлении поручения."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ORDER_ID_FIELD_NUMBER: builtins.int
    EXECUTION_REPORT_STATUS_FIELD_NUMBER: builtins.int
    LOTS_REQUESTED_FIELD_NUMBER: builtins.int
    LOTS_EXECUTED_FIELD_NUMBER: builtins.int
    INITIAL_ORDER_PRICE_FIELD_NUMBER: builtins.int
    EXECUTED_ORDER_PRICE_FIELD_NUMBER: builtins.int
    TOTAL_ORDER_AMOUNT_FIELD_NUMBER: builtins.int
    INITIAL_COMMISSION_FIELD_NUMBER: builtins.int
    EXECUTED_COMMISSION_FIELD_NUMBER: builtins.int
    ACI_VALUE_FIELD_NUMBER: builtins.int
    FIGI_FIELD_NUMBER: builtins.int
    DIRECTION_FIELD_NUMBER: builtins.int
    INITIAL_SECURITY_PRICE_FIELD_NUMBER: builtins.int
    ORDER_TYPE_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    INITIAL_ORDER_PRICE_PT_FIELD_NUMBER: builtins.int
    INSTRUMENT_UID_FIELD_NUMBER: builtins.int
    order_id: builtins.str
    """Идентификатор заявки."""
    execution_report_status: global___OrderExecutionReportStatus.ValueType
    """Текущий статус заявки."""
    lots_requested: builtins.int
    """Запрошено лотов."""
    lots_executed: builtins.int
    """Исполнено лотов."""
    @property
    def initial_order_price(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Начальная цена заявки. Произведение количества запрошенных лотов на цену."""
    @property
    def executed_order_price(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Исполненная средняя цена 1 одного инструмента в заявки."""
    @property
    def total_order_amount(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Итоговая стоимость заявки, включающая все комиссии."""
    @property
    def initial_commission(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Начальная комиссия. Комиссия рассчитанная при выставлении заявки."""
    @property
    def executed_commission(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Фактическая комиссия по итогам исполнения заявки."""
    @property
    def aci_value(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Значение НКД (накопленного купонного дохода) на дату. Подробнее: [НКД при выставлении торговых поручений](https://tinkoff.github.io/investAPI/head-orders#coupon)"""
    figi: builtins.str
    """Figi-идентификатор инструмента."""
    direction: global___OrderDirection.ValueType
    """Направление сделки."""
    @property
    def initial_security_price(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Начальная цена за 1 инструмент. Для получения стоимости лота требуется умножить на лотность инструмента."""
    order_type: global___OrderType.ValueType
    """Тип заявки."""
    message: builtins.str
    """Дополнительные данные об исполнении заявки."""
    @property
    def initial_order_price_pt(self) -> tinkoff.invest.grpc.common_pb2.Quotation:
        """Начальная цена заявки в пунктах (для фьючерсов)."""
    instrument_uid: builtins.str
    """UID идентификатор инструмента."""
    def __init__(
        self,
        *,
        order_id: builtins.str = ...,
        execution_report_status: global___OrderExecutionReportStatus.ValueType = ...,
        lots_requested: builtins.int = ...,
        lots_executed: builtins.int = ...,
        initial_order_price: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        executed_order_price: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        total_order_amount: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        initial_commission: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        executed_commission: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        aci_value: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        figi: builtins.str = ...,
        direction: global___OrderDirection.ValueType = ...,
        initial_security_price: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        order_type: global___OrderType.ValueType = ...,
        message: builtins.str = ...,
        initial_order_price_pt: tinkoff.invest.grpc.common_pb2.Quotation | None = ...,
        instrument_uid: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["aci_value", b"aci_value", "executed_commission", b"executed_commission", "executed_order_price", b"executed_order_price", "initial_commission", b"initial_commission", "initial_order_price", b"initial_order_price", "initial_order_price_pt", b"initial_order_price_pt", "initial_security_price", b"initial_security_price", "total_order_amount", b"total_order_amount"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["aci_value", b"aci_value", "direction", b"direction", "executed_commission", b"executed_commission", "executed_order_price", b"executed_order_price", "execution_report_status", b"execution_report_status", "figi", b"figi", "initial_commission", b"initial_commission", "initial_order_price", b"initial_order_price", "initial_order_price_pt", b"initial_order_price_pt", "initial_security_price", b"initial_security_price", "instrument_uid", b"instrument_uid", "lots_executed", b"lots_executed", "lots_requested", b"lots_requested", "message", b"message", "order_id", b"order_id", "order_type", b"order_type", "total_order_amount", b"total_order_amount"]) -> None: ...

global___PostOrderResponse = PostOrderResponse

class CancelOrderRequest(google.protobuf.message.Message):
    """Запрос отмены торгового поручения."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCOUNT_ID_FIELD_NUMBER: builtins.int
    ORDER_ID_FIELD_NUMBER: builtins.int
    account_id: builtins.str
    """Номер счёта."""
    order_id: builtins.str
    """Идентификатор заявки."""
    def __init__(
        self,
        *,
        account_id: builtins.str = ...,
        order_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_id", b"account_id", "order_id", b"order_id"]) -> None: ...

global___CancelOrderRequest = CancelOrderRequest

class CancelOrderResponse(google.protobuf.message.Message):
    """Результат отмены торгового поручения."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TIME_FIELD_NUMBER: builtins.int
    @property
    def time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Дата и время отмены заявки в часовом поясе UTC."""
    def __init__(
        self,
        *,
        time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["time", b"time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["time", b"time"]) -> None: ...

global___CancelOrderResponse = CancelOrderResponse

class GetOrderStateRequest(google.protobuf.message.Message):
    """Запрос получения статуса торгового поручения."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCOUNT_ID_FIELD_NUMBER: builtins.int
    ORDER_ID_FIELD_NUMBER: builtins.int
    account_id: builtins.str
    """Номер счёта."""
    order_id: builtins.str
    """Идентификатор заявки."""
    def __init__(
        self,
        *,
        account_id: builtins.str = ...,
        order_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_id", b"account_id", "order_id", b"order_id"]) -> None: ...

global___GetOrderStateRequest = GetOrderStateRequest

class GetOrdersRequest(google.protobuf.message.Message):
    """Запрос получения списка активных торговых поручений."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCOUNT_ID_FIELD_NUMBER: builtins.int
    account_id: builtins.str
    """Номер счёта."""
    def __init__(
        self,
        *,
        account_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_id", b"account_id"]) -> None: ...

global___GetOrdersRequest = GetOrdersRequest

class GetOrdersResponse(google.protobuf.message.Message):
    """Список активных торговых поручений."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ORDERS_FIELD_NUMBER: builtins.int
    @property
    def orders(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OrderState]:
        """Массив активных заявок."""
    def __init__(
        self,
        *,
        orders: collections.abc.Iterable[global___OrderState] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["orders", b"orders"]) -> None: ...

global___GetOrdersResponse = GetOrdersResponse

class OrderState(google.protobuf.message.Message):
    """Информация о торговом поручении."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ORDER_ID_FIELD_NUMBER: builtins.int
    EXECUTION_REPORT_STATUS_FIELD_NUMBER: builtins.int
    LOTS_REQUESTED_FIELD_NUMBER: builtins.int
    LOTS_EXECUTED_FIELD_NUMBER: builtins.int
    INITIAL_ORDER_PRICE_FIELD_NUMBER: builtins.int
    EXECUTED_ORDER_PRICE_FIELD_NUMBER: builtins.int
    TOTAL_ORDER_AMOUNT_FIELD_NUMBER: builtins.int
    AVERAGE_POSITION_PRICE_FIELD_NUMBER: builtins.int
    INITIAL_COMMISSION_FIELD_NUMBER: builtins.int
    EXECUTED_COMMISSION_FIELD_NUMBER: builtins.int
    FIGI_FIELD_NUMBER: builtins.int
    DIRECTION_FIELD_NUMBER: builtins.int
    INITIAL_SECURITY_PRICE_FIELD_NUMBER: builtins.int
    STAGES_FIELD_NUMBER: builtins.int
    SERVICE_COMMISSION_FIELD_NUMBER: builtins.int
    CURRENCY_FIELD_NUMBER: builtins.int
    ORDER_TYPE_FIELD_NUMBER: builtins.int
    ORDER_DATE_FIELD_NUMBER: builtins.int
    INSTRUMENT_UID_FIELD_NUMBER: builtins.int
    order_id: builtins.str
    """Идентификатор заявки."""
    execution_report_status: global___OrderExecutionReportStatus.ValueType
    """Текущий статус заявки."""
    lots_requested: builtins.int
    """Запрошено лотов."""
    lots_executed: builtins.int
    """Исполнено лотов."""
    @property
    def initial_order_price(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Начальная цена заявки. Произведение количества запрошенных лотов на цену."""
    @property
    def executed_order_price(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Исполненная цена заявки. Произведение средней цены покупки на количество лотов."""
    @property
    def total_order_amount(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Итоговая стоимость заявки, включающая все комиссии."""
    @property
    def average_position_price(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Средняя цена позиции по сделке."""
    @property
    def initial_commission(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Начальная комиссия. Комиссия, рассчитанная на момент подачи заявки."""
    @property
    def executed_commission(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Фактическая комиссия по итогам исполнения заявки."""
    figi: builtins.str
    """Figi-идентификатор инструмента."""
    direction: global___OrderDirection.ValueType
    """Направление заявки."""
    @property
    def initial_security_price(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Начальная цена за 1 инструмент. Для получения стоимости лота требуется умножить на лотность инструмента."""
    @property
    def stages(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___OrderStage]:
        """Стадии выполнения заявки."""
    @property
    def service_commission(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Сервисная комиссия."""
    currency: builtins.str
    """Валюта заявки."""
    order_type: global___OrderType.ValueType
    """Тип заявки."""
    @property
    def order_date(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Дата и время выставления заявки в часовом поясе UTC."""
    instrument_uid: builtins.str
    """UID идентификатор инструмента."""
    def __init__(
        self,
        *,
        order_id: builtins.str = ...,
        execution_report_status: global___OrderExecutionReportStatus.ValueType = ...,
        lots_requested: builtins.int = ...,
        lots_executed: builtins.int = ...,
        initial_order_price: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        executed_order_price: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        total_order_amount: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        average_position_price: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        initial_commission: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        executed_commission: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        figi: builtins.str = ...,
        direction: global___OrderDirection.ValueType = ...,
        initial_security_price: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        stages: collections.abc.Iterable[global___OrderStage] | None = ...,
        service_commission: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        currency: builtins.str = ...,
        order_type: global___OrderType.ValueType = ...,
        order_date: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        instrument_uid: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["average_position_price", b"average_position_price", "executed_commission", b"executed_commission", "executed_order_price", b"executed_order_price", "initial_commission", b"initial_commission", "initial_order_price", b"initial_order_price", "initial_security_price", b"initial_security_price", "order_date", b"order_date", "service_commission", b"service_commission", "total_order_amount", b"total_order_amount"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["average_position_price", b"average_position_price", "currency", b"currency", "direction", b"direction", "executed_commission", b"executed_commission", "executed_order_price", b"executed_order_price", "execution_report_status", b"execution_report_status", "figi", b"figi", "initial_commission", b"initial_commission", "initial_order_price", b"initial_order_price", "initial_security_price", b"initial_security_price", "instrument_uid", b"instrument_uid", "lots_executed", b"lots_executed", "lots_requested", b"lots_requested", "order_date", b"order_date", "order_id", b"order_id", "order_type", b"order_type", "service_commission", b"service_commission", "stages", b"stages", "total_order_amount", b"total_order_amount"]) -> None: ...

global___OrderState = OrderState

class OrderStage(google.protobuf.message.Message):
    """Сделки в рамках торгового поручения."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PRICE_FIELD_NUMBER: builtins.int
    QUANTITY_FIELD_NUMBER: builtins.int
    TRADE_ID_FIELD_NUMBER: builtins.int
    @property
    def price(self) -> tinkoff.invest.grpc.common_pb2.MoneyValue:
        """Цена за 1 инструмент. Для получения стоимости лота требуется умножить на лотность инструмента.."""
    quantity: builtins.int
    """Количество лотов."""
    trade_id: builtins.str
    """Идентификатор сделки."""
    def __init__(
        self,
        *,
        price: tinkoff.invest.grpc.common_pb2.MoneyValue | None = ...,
        quantity: builtins.int = ...,
        trade_id: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["price", b"price"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["price", b"price", "quantity", b"quantity", "trade_id", b"trade_id"]) -> None: ...

global___OrderStage = OrderStage

class ReplaceOrderRequest(google.protobuf.message.Message):
    """Запрос изменения выставленной заявки."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACCOUNT_ID_FIELD_NUMBER: builtins.int
    ORDER_ID_FIELD_NUMBER: builtins.int
    IDEMPOTENCY_KEY_FIELD_NUMBER: builtins.int
    QUANTITY_FIELD_NUMBER: builtins.int
    PRICE_FIELD_NUMBER: builtins.int
    PRICE_TYPE_FIELD_NUMBER: builtins.int
    account_id: builtins.str
    """Номер счета."""
    order_id: builtins.str
    """Идентификатор заявки на бирже."""
    idempotency_key: builtins.str
    """Новый идентификатор запроса выставления поручения для целей идемпотентности. Максимальная длина 36 символов. Перезатирает старый ключ."""
    quantity: builtins.int
    """Количество лотов."""
    @property
    def price(self) -> tinkoff.invest.grpc.common_pb2.Quotation:
        """Цена за 1 инструмент."""
    price_type: global___PriceType.ValueType
    """Тип цены."""
    def __init__(
        self,
        *,
        account_id: builtins.str = ...,
        order_id: builtins.str = ...,
        idempotency_key: builtins.str = ...,
        quantity: builtins.int = ...,
        price: tinkoff.invest.grpc.common_pb2.Quotation | None = ...,
        price_type: global___PriceType.ValueType = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["price", b"price"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_id", b"account_id", "idempotency_key", b"idempotency_key", "order_id", b"order_id", "price", b"price", "price_type", b"price_type", "quantity", b"quantity"]) -> None: ...

global___ReplaceOrderRequest = ReplaceOrderRequest
