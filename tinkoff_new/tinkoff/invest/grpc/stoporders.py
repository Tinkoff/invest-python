"""
DO NOT EDIT!
Generated by ohmyproto
isort:skip_file
"""
import proto
from google.protobuf import timestamp_pb2
from tinkoff.invest.grpc import common

__protobuf__ = proto.module(package=__name__)


class StopOrderDirection(proto.Enum):
    """Направление сделки стоп-заявки."""

    STOP_ORDER_DIRECTION_UNSPECIFIED = 0
    """Значение не указано."""

    STOP_ORDER_DIRECTION_BUY = 1
    """Покупка."""

    STOP_ORDER_DIRECTION_SELL = 2
    """Продажа."""


class StopOrderExpirationType(proto.Enum):
    """Тип экспирации стоп-заявке."""

    STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED = 0
    """Значение не указано."""

    STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL = 1
    """Действительно до отмены."""

    STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_DATE = 2
    """Действительно до даты снятия."""


class StopOrderType(proto.Enum):
    """Тип стоп-заявки."""

    STOP_ORDER_TYPE_UNSPECIFIED = 0
    """Значение не указано."""

    STOP_ORDER_TYPE_TAKE_PROFIT = 1
    """Take-profit заявка."""

    STOP_ORDER_TYPE_STOP_LOSS = 2
    """Stop-loss заявка."""

    STOP_ORDER_TYPE_STOP_LIMIT = 3
    """Stop-limit заявка."""


class StopOrder(proto.Message):
    """Информация о стоп-заявке."""

    stop_order_id = proto.Field(proto.STRING, number=1)
    """Идентификатор-идентификатор стоп-заявки."""

    lots_requested = proto.Field(proto.INT64, number=2)
    """Запрошено лотов."""

    figi = proto.Field(proto.STRING, number=3)
    """Figi-идентификатор инструмента."""

    direction = proto.Field(StopOrderDirection, number=4)
    """Направление операции."""

    currency = proto.Field(proto.STRING, number=5)
    """Валюта стоп-заявки."""

    order_type = proto.Field(StopOrderType, number=6)
    """Тип стоп-заявки."""

    create_date = proto.Field(timestamp_pb2.Timestamp, number=7)
    """Дата и время выставления заявки в часовом поясе UTC."""

    activation_date_time = proto.Field(timestamp_pb2.Timestamp, number=8)
    """Дата и время конвертации стоп-заявки в биржевую в часовом поясе UTC."""

    expiration_time = proto.Field(timestamp_pb2.Timestamp, number=9)
    """Дата и время снятия заявки в часовом поясе UTC."""

    price = proto.Field(common.MoneyValue, number=10)
    """Цена заявки за 1 инструмент. Для получения стоимости лота требуется умножить на лотность инструмента."""

    stop_price = proto.Field(common.MoneyValue, number=11)
    """Цена активации стоп-заявки за 1 инструмент. Для получения стоимости лота требуется умножить на лотность инструмента."""


class PostStopOrderRequest(proto.Message):
    """Запрос выставления стоп-заявки."""

    figi = proto.Field(proto.STRING, number=1)
    """Figi-идентификатор инструмента."""

    quantity = proto.Field(proto.INT64, number=2)
    """Количество лотов."""

    price = proto.Field(common.Quotation, number=3)
    """Цена за 1 инструмент. Для получения стоимости лота требуется умножить на лотность инструмента."""

    stop_price = proto.Field(common.Quotation, number=4)
    """Стоп-цена заявки за 1 инструмент. Для получения стоимости лота требуется умножить на лотность инструмента."""

    direction = proto.Field(StopOrderDirection, number=5)
    """Направление операции."""

    account_id = proto.Field(proto.STRING, number=6)
    """Номер счёта."""

    expiration_type = proto.Field(StopOrderExpirationType, number=7)
    """Тип экспирации заявки."""

    stop_order_type = proto.Field(StopOrderType, number=8)
    """Тип заявки."""

    expire_date = proto.Field(timestamp_pb2.Timestamp, number=9)
    """Дата и время окончания действия стоп-заявки в часовом поясе UTC. **Для ExpirationType = GoodTillDate заполнение обязательно**."""


class PostStopOrderResponse(proto.Message):
    """Результат выставления стоп-заявки."""

    stop_order_id = proto.Field(proto.STRING, number=1)
    """Уникальный идентификатор стоп-заявки."""


class GetStopOrdersRequest(proto.Message):
    """Запрос получения списка активных стоп-заявок."""

    account_id = proto.Field(proto.STRING, number=1)
    """Идентификатор счёта клиента."""


class CancelStopOrderRequest(proto.Message):
    """Запрос отмены выставленной стоп-заявки."""

    account_id = proto.Field(proto.STRING, number=1)
    """Идентификатор счёта клиента."""

    stop_order_id = proto.Field(proto.STRING, number=2)
    """Уникальный идентификатор стоп-заявки."""


class CancelStopOrderResponse(proto.Message):
    """Результат отмены выставленной стоп-заявки."""

    time = proto.Field(timestamp_pb2.Timestamp, number=1)
    """Время отмены заявки в часовом поясе UTC."""


class GetStopOrdersResponse(proto.Message):
    """Список активных стоп-заявок."""

    stop_orders = proto.RepeatedField(StopOrder, number=1)
    """Массив стоп-заявок по счёту."""

