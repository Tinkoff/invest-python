# pylint:disable=too-many-lines
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

from . import grpc_helpers


class SecurityTradingStatus(grpc_helpers.Enum):
    SECURITY_TRADING_STATUS_UNSPECIFIED = 0
    SECURITY_TRADING_STATUS_NOT_AVAILABLE_FOR_TRADING = 1
    SECURITY_TRADING_STATUS_OPENING_PERIOD = 2
    SECURITY_TRADING_STATUS_CLOSING_PERIOD = 3
    SECURITY_TRADING_STATUS_BREAK_IN_TRADING = 4
    SECURITY_TRADING_STATUS_NORMAL_TRADING = 5
    SECURITY_TRADING_STATUS_CLOSING_AUCTION = 6
    SECURITY_TRADING_STATUS_DARK_POOL_AUCTION = 7
    SECURITY_TRADING_STATUS_DISCRETE_AUCTION = 8
    SECURITY_TRADING_STATUS_OPENING_AUCTION_PERIOD = 9
    SECURITY_TRADING_STATUS_TRADING_AT_CLOSING_AUCTION_PRICE = 10


class InstrumentIdType(grpc_helpers.Enum):
    INSTRUMENT_ID_UNSPECIFIED = 0
    INSTRUMENT_ID_TYPE_FIGI = 1
    INSTRUMENT_ID_TYPE_TICKER = 2


class InstrumentStatus(grpc_helpers.Enum):
    INSTRUMENT_STATUS_UNSPECIFIED = 0
    INSTRUMENT_STATUS_BASE = 1
    INSTRUMENT_STATUS_ALL = 2


class ShareType(grpc_helpers.Enum):
    SHARE_TYPE_UNSPECIFIED = 0
    SHARE_TYPE_COMMON = 1
    SHARE_TYPE_PREFERRED = 2
    SHARE_TYPE_ADR = 3
    SHARE_TYPE_GDR = 4
    SHARE_TYPE_MLP = 5
    SHARE_TYPE_NY_REG_SHRS = 6
    SHARE_TYPE_CLOSED_END_FUND = 7
    SHARE_TYPE_REIT = 8


class SubscriptionAction(grpc_helpers.Enum):
    SUBSCRIPTION_ACTION_UNSPECIFIED = 0
    SUBSCRIPTION_ACTION_SUBSCRIBE = 1
    SUBSCRIPTION_ACTION_UNSUBSCRIBE = 2


class SubscriptionInterval(grpc_helpers.Enum):
    SUBSCRIPTION_INTERVAL_UNSPECIFIED = 0
    SUBSCRIPTION_INTERVAL_ONE_MINUTE = 1
    SUBSCRIPTION_INTERVAL_FIVE_MINUTES = 2


class SubscriptionStatus(grpc_helpers.Enum):
    SUBSCRIPTION_STATUS_UNSPECIFIED = 0
    SUBSCRIPTION_STATUS_SUCCESS = 1
    SUBSCRIPTION_STATUS_INSTRUMENT_NOT_FOUND = 2
    SUBSCRIPTION_STATUS_SUBSCRIPTION_ACTION_IS_INVALID = 3
    SUBSCRIPTION_STATUS_DEPTH_IS_INVALID = 4
    SUBSCRIPTION_STATUS_INTERVAL_IS_INVALID = 5
    SUBSCRIPTION_STATUS_LIMIT_IS_EXCEEDED = 6
    SUBSCRIPTION_STATUS_INTERNAL_ERROR = 7


class TradeDirection(grpc_helpers.Enum):
    TRADE_DIRECTION_UNSPECIFIED = 0
    TRADE_DIRECTION_BUY = 1
    TRADE_DIRECTION_SELL = 2


class CandleInterval(grpc_helpers.Enum):
    CANDLE_INTERVAL_UNSPECIFIED = 0
    CANDLE_INTERVAL_1_MIN = 1
    CANDLE_INTERVAL_5_MIN = 2
    CANDLE_INTERVAL_15_MIN = 3
    CANDLE_INTERVAL_HOUR = 4
    CANDLE_INTERVAL_DAY = 5


class OperationState(grpc_helpers.Enum):
    OPERATION_STATE_UNSPECIFIED = 0
    OPERATION_STATE_EXECUTED = 1
    OPERATION_STATE_CANCELED = 2


class OrderDirection(grpc_helpers.Enum):
    ORDER_DIRECTION_UNSPECIFIED = 0
    ORDER_DIRECTION_BUY = 1
    ORDER_DIRECTION_SELL = 2


class OrderType(grpc_helpers.Enum):
    ORDER_TYPE_UNSPECIFIED = 0
    ORDER_TYPE_LIMIT = 1
    ORDER_TYPE_MARKET = 2


class OrderExecutionReportStatus(grpc_helpers.Enum):
    EXECUTION_REPORT_STATUS_UNSPECIFIED = 0
    EXECUTION_REPORT_STATUS_FILL = 1
    EXECUTION_REPORT_STATUS_REJECTED = 2
    EXECUTION_REPORT_STATUS_CANCELLED = 3
    EXECUTION_REPORT_STATUS_NEW = 4
    EXECUTION_REPORT_STATUS_PARTIALLYFILL = 5


class AccountType(grpc_helpers.Enum):
    ACCOUNT_TYPE_UNSPECIFIED = 0
    ACCOUNT_TYPE_TINKOFF = 1
    ACCOUNT_TYPE_TINKOFF_IIS = 2
    ACCOUNT_TYPE_INVEST_BOX = 3


class AccountStatus(grpc_helpers.Enum):
    ACCOUNT_STATUS_UNSPECIFIED = 0
    ACCOUNT_STATUS_NEW = 1
    ACCOUNT_STATUS_OPEN = 2
    ACCOUNT_STATUS_CLOSED = 3


class StopOrderDirection(grpc_helpers.Enum):
    STOP_ORDER_DIRECTION_UNSPECIFIED = 0
    STOP_ORDER_DIRECTION_BUY = 1
    STOP_ORDER_DIRECTION_SELL = 2


class StopOrderExpirationType(grpc_helpers.Enum):
    STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED = 0
    STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL = 1
    STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_DATE = 2


class StopOrderType(grpc_helpers.Enum):
    STOP_ORDER_TYPE_UNSPECIFIED = 0
    STOP_ORDER_TYPE_TAKE_PROFIT = 1
    STOP_ORDER_TYPE_STOP_LOSS = 2
    STOP_ORDER_TYPE_STOP_LIMIT = 3


@dataclass(eq=False, repr=True)
class MoneyValue(grpc_helpers.Message):
    currency: str = grpc_helpers.string_field(1)
    units: int = grpc_helpers.int64_field(2)
    nano: int = grpc_helpers.int32_field(3)


@dataclass(eq=False, repr=True)
class Quotation(grpc_helpers.Message):
    units: int = grpc_helpers.int64_field(1)
    nano: int = grpc_helpers.int32_field(2)


@dataclass(eq=False, repr=True)
class TradingSchedulesRequest(grpc_helpers.Message):
    exchange: str = grpc_helpers.string_field(1)
    from_: datetime = grpc_helpers.message_field(2)
    to: datetime = grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class TradingSchedulesResponse(grpc_helpers.Message):
    exchanges: List["TradingSchedule"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class TradingSchedule(grpc_helpers.Message):
    exchange: str = grpc_helpers.string_field(1)
    days: List["TradingDay"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class TradingDay(grpc_helpers.Message):
    date: datetime = grpc_helpers.message_field(1)
    is_trading_day: bool = grpc_helpers.bool_field(2)
    start_time: datetime = grpc_helpers.message_field(3)
    end_time: datetime = grpc_helpers.message_field(4)
    market_order_start_time: datetime = grpc_helpers.message_field(5)
    market_order_end_time: datetime = grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class InstrumentRequest(grpc_helpers.Message):
    id_type: "InstrumentIdType" = grpc_helpers.enum_field(1)
    class_code: str = grpc_helpers.string_field(2)
    id: str = grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class InstrumentsRequest(grpc_helpers.Message):
    instrument_status: "InstrumentStatus" = grpc_helpers.enum_field(1)


@dataclass(eq=False, repr=True)
class BondResponse(grpc_helpers.Message):
    instrument: "Bond" = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class BondsResponse(grpc_helpers.Message):
    instruments: List["Bond"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class CurrencyResponse(grpc_helpers.Message):
    instrument: "Currency" = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class CurrenciesResponse(grpc_helpers.Message):
    instruments: List["Currency"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class EtfResponse(grpc_helpers.Message):
    instrument: "Etf" = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class EtfsResponse(grpc_helpers.Message):
    instruments: List["Etf"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class FutureResponse(grpc_helpers.Message):
    instrument: "Future" = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class FuturesResponse(grpc_helpers.Message):
    instruments: List["Future"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class ShareResponse(grpc_helpers.Message):
    instrument: "Share" = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class SharesResponse(grpc_helpers.Message):
    instruments: List["Share"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Bond(grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = grpc_helpers.string_field(1)
    ticker: str = grpc_helpers.string_field(2)
    class_code: str = grpc_helpers.string_field(3)
    isin: str = grpc_helpers.string_field(4)
    lot: int = grpc_helpers.int32_field(5)
    currency: str = grpc_helpers.string_field(6)
    klong: Decimal = grpc_helpers.double_field(7)
    kshort: Decimal = grpc_helpers.double_field(8)
    dlong: Decimal = grpc_helpers.double_field(9)
    dshort: Decimal = grpc_helpers.double_field(10)
    dlong_min: Decimal = grpc_helpers.double_field(11)
    dshort_min: Decimal = grpc_helpers.double_field(12)
    short_enabled_flag: bool = grpc_helpers.bool_field(13)
    name: str = grpc_helpers.string_field(15)
    exchange: str = grpc_helpers.string_field(16)
    coupon_quantity_per_year: int = grpc_helpers.int32_field(17)
    maturity_date: datetime = grpc_helpers.message_field(18)
    nominal: "MoneyValue" = grpc_helpers.message_field(19)
    state_reg_date: datetime = grpc_helpers.message_field(21)
    placement_date: datetime = grpc_helpers.message_field(22)
    placement_price: "MoneyValue" = grpc_helpers.message_field(23)
    aci_value: "MoneyValue" = grpc_helpers.message_field(24)
    country_of_risk: str = grpc_helpers.string_field(25)
    country_of_risk_name: str = grpc_helpers.string_field(26)
    sector: str = grpc_helpers.string_field(27)
    issue_kind: str = grpc_helpers.string_field(28)
    issue_size: int = grpc_helpers.int64_field(29)
    issue_size_plan: int = grpc_helpers.int64_field(30)
    trading_status: "SecurityTradingStatus" = grpc_helpers.enum_field(31)
    otc_flag: bool = grpc_helpers.bool_field(32)
    buy_available_flag: bool = grpc_helpers.bool_field(33)
    sell_available_flag: bool = grpc_helpers.bool_field(34)
    floating_coupon_flag: bool = grpc_helpers.bool_field(35)
    perpetual_flag: bool = grpc_helpers.bool_field(36)
    amortization_flag: bool = grpc_helpers.bool_field(37)
    min_price_increment: Decimal = grpc_helpers.float_field(38)
    api_trade_available_flag: bool = grpc_helpers.bool_field(39)


@dataclass(eq=False, repr=True)
class Currency(grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = grpc_helpers.string_field(1)
    ticker: str = grpc_helpers.string_field(2)
    class_code: str = grpc_helpers.string_field(3)
    isin: str = grpc_helpers.string_field(4)
    lot: int = grpc_helpers.int32_field(5)
    currency: str = grpc_helpers.string_field(6)
    klong: Decimal = grpc_helpers.double_field(7)
    kshort: Decimal = grpc_helpers.double_field(8)
    dlong: Decimal = grpc_helpers.double_field(9)
    dshort: Decimal = grpc_helpers.double_field(10)
    dlong_min: Decimal = grpc_helpers.double_field(11)
    dshort_min: Decimal = grpc_helpers.double_field(12)
    short_enabled_flag: bool = grpc_helpers.bool_field(13)
    name: str = grpc_helpers.string_field(15)
    exchange: str = grpc_helpers.string_field(16)
    nominal: "MoneyValue" = grpc_helpers.message_field(17)
    country_of_risk: str = grpc_helpers.string_field(18)
    country_of_risk_name: str = grpc_helpers.string_field(19)
    trading_status: "SecurityTradingStatus" = grpc_helpers.enum_field(20)
    otc_flag: bool = grpc_helpers.bool_field(21)
    buy_available_flag: bool = grpc_helpers.bool_field(22)
    sell_available_flag: bool = grpc_helpers.bool_field(23)
    iso_currency_name: str = grpc_helpers.string_field(24)
    min_price_increment: Decimal = grpc_helpers.float_field(25)
    api_trade_available_flag: bool = grpc_helpers.bool_field(26)


@dataclass(eq=False, repr=True)
class Etf(grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = grpc_helpers.string_field(1)
    ticker: str = grpc_helpers.string_field(2)
    class_code: str = grpc_helpers.string_field(3)
    isin: str = grpc_helpers.string_field(4)
    lot: int = grpc_helpers.int32_field(5)
    currency: str = grpc_helpers.string_field(6)
    klong: Decimal = grpc_helpers.double_field(7)
    kshort: Decimal = grpc_helpers.double_field(8)
    dlong: Decimal = grpc_helpers.double_field(9)
    dshort: Decimal = grpc_helpers.double_field(10)
    dlong_min: Decimal = grpc_helpers.double_field(11)
    dshort_min: Decimal = grpc_helpers.double_field(12)
    short_enabled_flag: bool = grpc_helpers.bool_field(13)
    name: str = grpc_helpers.string_field(15)
    exchange: str = grpc_helpers.string_field(16)
    fixed_commission: Decimal = grpc_helpers.double_field(17)
    focus_type: str = grpc_helpers.string_field(18)
    released_date: datetime = grpc_helpers.message_field(19)
    num_shares: Decimal = grpc_helpers.double_field(20)
    country_of_risk: str = grpc_helpers.string_field(21)
    country_of_risk_name: str = grpc_helpers.string_field(22)
    sector: str = grpc_helpers.string_field(23)
    rebalancing_freq: str = grpc_helpers.string_field(24)
    trading_status: "SecurityTradingStatus" = grpc_helpers.enum_field(25)
    otc_flag: bool = grpc_helpers.bool_field(26)
    buy_available_flag: bool = grpc_helpers.bool_field(27)
    sell_available_flag: bool = grpc_helpers.bool_field(28)
    min_price_increment: Decimal = grpc_helpers.float_field(29)
    api_trade_available_flag: bool = grpc_helpers.bool_field(30)


@dataclass(eq=False, repr=True)
class Future(grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = grpc_helpers.string_field(1)
    ticker: str = grpc_helpers.string_field(2)
    class_code: str = grpc_helpers.string_field(3)
    lot: int = grpc_helpers.int32_field(4)
    currency: str = grpc_helpers.string_field(5)
    klong: Decimal = grpc_helpers.double_field(6)
    kshort: Decimal = grpc_helpers.double_field(7)
    dlong: Decimal = grpc_helpers.double_field(8)
    dshort: Decimal = grpc_helpers.double_field(9)
    dlong_min: Decimal = grpc_helpers.double_field(10)
    dshort_min: Decimal = grpc_helpers.double_field(11)
    short_enabled_flag: bool = grpc_helpers.bool_field(12)
    name: str = grpc_helpers.string_field(13)
    exchange: str = grpc_helpers.string_field(14)
    first_trade_date: datetime = grpc_helpers.message_field(15)
    last_trade_date: datetime = grpc_helpers.message_field(16)
    futures_type: str = grpc_helpers.string_field(17)
    asset_type: str = grpc_helpers.string_field(18)
    basic_asset: str = grpc_helpers.string_field(19)
    basic_asset_size: Decimal = grpc_helpers.double_field(20)
    country_of_risk: str = grpc_helpers.string_field(21)
    country_of_risk_name: str = grpc_helpers.string_field(22)
    sector: str = grpc_helpers.string_field(23)
    expiration_date: datetime = grpc_helpers.message_field(24)
    trading_status: "SecurityTradingStatus" = grpc_helpers.enum_field(25)
    otc_flag: bool = grpc_helpers.bool_field(26)
    buy_available_flag: bool = grpc_helpers.bool_field(27)
    sell_available_flag: bool = grpc_helpers.bool_field(28)
    min_price_increment: Decimal = grpc_helpers.float_field(29)
    api_trade_available_flag: bool = grpc_helpers.bool_field(30)


@dataclass(eq=False, repr=True)
class Share(grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = grpc_helpers.string_field(1)
    ticker: str = grpc_helpers.string_field(2)
    class_code: str = grpc_helpers.string_field(3)
    isin: str = grpc_helpers.string_field(4)
    lot: int = grpc_helpers.int32_field(5)
    currency: str = grpc_helpers.string_field(6)
    klong: Decimal = grpc_helpers.double_field(7)
    kshort: Decimal = grpc_helpers.double_field(8)
    dlong: Decimal = grpc_helpers.double_field(9)
    dshort: Decimal = grpc_helpers.double_field(10)
    dlong_min: Decimal = grpc_helpers.double_field(11)
    dshort_min: Decimal = grpc_helpers.double_field(12)
    short_enabled_flag: bool = grpc_helpers.bool_field(13)
    name: str = grpc_helpers.string_field(15)
    exchange: str = grpc_helpers.string_field(16)
    ipo_date: datetime = grpc_helpers.message_field(17)
    issue_size: int = grpc_helpers.int64_field(18)
    country_of_risk: str = grpc_helpers.string_field(19)
    country_of_risk_name: str = grpc_helpers.string_field(20)
    sector: str = grpc_helpers.string_field(21)
    issue_size_plan: int = grpc_helpers.int64_field(22)
    nominal: "MoneyValue" = grpc_helpers.message_field(23)
    trading_status: "SecurityTradingStatus" = grpc_helpers.enum_field(25)
    otc_flag: bool = grpc_helpers.bool_field(26)
    buy_available_flag: bool = grpc_helpers.bool_field(27)
    sell_available_flag: bool = grpc_helpers.bool_field(28)
    div_yield_flag: bool = grpc_helpers.bool_field(29)
    share_type: "ShareType" = grpc_helpers.enum_field(30)
    min_price_increment: Decimal = grpc_helpers.float_field(31)
    api_trade_available_flag: bool = grpc_helpers.bool_field(32)


@dataclass(eq=False, repr=True)
class GetAccruedInterestsRequest(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    from_: datetime = grpc_helpers.message_field(2)
    to: datetime = grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class GetAccruedInterestsResponse(grpc_helpers.Message):
    accrued_interests: List["AccruedInterest"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class AccruedInterest(grpc_helpers.Message):
    date: datetime = grpc_helpers.message_field(1)
    value: "Quotation" = grpc_helpers.message_field(2)
    value_percent: Decimal = grpc_helpers.float_field(3)
    nominal: "Quotation" = grpc_helpers.message_field(4)


@dataclass(eq=False, repr=True)
class GetFuturesMarginRequest(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetFuturesMarginResponse(grpc_helpers.Message):
    initial_margin_on_buy: "MoneyValue" = grpc_helpers.message_field(1)
    initial_margin_on_sell: "MoneyValue" = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class InstrumentResponse(grpc_helpers.Message):
    instrument: "Instrument" = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Instrument(grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = grpc_helpers.string_field(1)
    ticker: str = grpc_helpers.string_field(2)
    class_code: str = grpc_helpers.string_field(3)
    isin: str = grpc_helpers.string_field(4)
    lot: int = grpc_helpers.int32_field(5)
    currency: str = grpc_helpers.string_field(6)
    klong: Decimal = grpc_helpers.double_field(7)
    kshort: Decimal = grpc_helpers.double_field(8)
    dlong: Decimal = grpc_helpers.double_field(9)
    dshort: Decimal = grpc_helpers.double_field(10)
    dlong_min: Decimal = grpc_helpers.double_field(11)
    dshort_min: Decimal = grpc_helpers.double_field(12)
    short_enabled_flag: bool = grpc_helpers.bool_field(13)
    name: str = grpc_helpers.string_field(14)
    exchange: str = grpc_helpers.string_field(15)
    country_of_risk: str = grpc_helpers.string_field(16)
    country_of_risk_name: str = grpc_helpers.string_field(17)
    instrument_type: str = grpc_helpers.string_field(18)
    trading_status: "SecurityTradingStatus" = grpc_helpers.enum_field(19)
    otc_flag: bool = grpc_helpers.bool_field(20)
    buy_available_flag: bool = grpc_helpers.bool_field(21)
    sell_available_flag: bool = grpc_helpers.bool_field(22)
    min_price_increment: Decimal = grpc_helpers.float_field(23)
    api_trade_available_flag: bool = grpc_helpers.bool_field(24)


@dataclass(eq=False, repr=True)
class GetDividendsRequest(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    from_: datetime = grpc_helpers.message_field(2)
    to: datetime = grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class GetDividendsResponse(grpc_helpers.Message):
    dividends: List["Dividend"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Dividend(grpc_helpers.Message):
    dividend_net: "MoneyValue" = grpc_helpers.message_field(1)
    payment_date: datetime = grpc_helpers.message_field(2)
    declared_date: datetime = grpc_helpers.message_field(3)
    last_buy_date: datetime = grpc_helpers.message_field(4)
    dividend_type: str = grpc_helpers.string_field(5)
    record_date: datetime = grpc_helpers.message_field(6)
    regularity: str = grpc_helpers.string_field(7)
    close_price: "MoneyValue" = grpc_helpers.message_field(8)
    yield_value: "Quotation" = grpc_helpers.message_field(9)
    created_at: datetime = grpc_helpers.message_field(10)


@dataclass(eq=False, repr=True)
class MarketDataRequest(grpc_helpers.Message):
    subscribe_candles_request: "SubscribeCandlesRequest" = grpc_helpers.message_field(
        1, group="payload"
    )
    subscribe_order_book_request: "SubscribeOrderBookRequest" = (
        grpc_helpers.message_field(2, group="payload")
    )
    subscribe_trades_request: "SubscribeTradesRequest" = grpc_helpers.message_field(
        3, group="payload"
    )
    subscribe_info_request: "SubscribeInfoRequest" = grpc_helpers.message_field(
        4, group="payload"
    )


@dataclass(eq=False, repr=True)
class MarketDataResponse(grpc_helpers.Message):
    subscribe_candles_response: "SubscribeCandlesResponse" = grpc_helpers.message_field(
        1, group="payload"
    )
    subscribe_order_book_response: "SubscribeOrderBookResponse" = (
        grpc_helpers.message_field(2, group="payload")
    )
    subscribe_trades_response: "SubscribeTradesResponse" = grpc_helpers.message_field(
        3, group="payload"
    )
    subscribe_info_response: "SubscribeInfoResponse" = grpc_helpers.message_field(
        4, group="payload"
    )
    candle: "Candle" = grpc_helpers.message_field(5, group="payload")
    trade: "Trade" = grpc_helpers.message_field(6, group="payload")
    orderbook: "OrderBook" = grpc_helpers.message_field(7, group="payload")
    trading_status: "TradingStatus" = grpc_helpers.message_field(8, group="payload")


@dataclass(eq=False, repr=True)
class SubscribeCandlesRequest(grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = grpc_helpers.enum_field(1)
    instruments: List["CandleInstrument"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class CandleInstrument(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    interval: "SubscriptionInterval" = grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class SubscribeCandlesResponse(grpc_helpers.Message):
    tracking_id: str = grpc_helpers.string_field(1)
    candles_subscriptions: List["CandleSubscription"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class CandleSubscription(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    interval: "SubscriptionInterval" = grpc_helpers.enum_field(2)
    subscription_status: "SubscriptionStatus" = grpc_helpers.enum_field(3)


@dataclass(eq=False, repr=True)
class SubscribeOrderBookRequest(grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = grpc_helpers.enum_field(1)
    instruments: List["OrderBookInstrument"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class OrderBookInstrument(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    depth: int = grpc_helpers.int32_field(2)


@dataclass(eq=False, repr=True)
class SubscribeOrderBookResponse(grpc_helpers.Message):
    tracking_id: str = grpc_helpers.string_field(1)
    order_book_subscriptions: List[
        "OrderBookSubscription"
    ] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class OrderBookSubscription(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    depth: int = grpc_helpers.int32_field(2)
    subscription_status: "SubscriptionStatus" = grpc_helpers.enum_field(3)


@dataclass(eq=False, repr=True)
class SubscribeTradesRequest(grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = grpc_helpers.enum_field(1)
    instruments: List["TradeInstrument"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class TradeInstrument(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class SubscribeTradesResponse(grpc_helpers.Message):
    tracking_id: str = grpc_helpers.string_field(1)
    trade_subscriptions: List["TradeSubscription"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class TradeSubscription(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    subscription_status: "SubscriptionStatus" = grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class SubscribeInfoRequest(grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = grpc_helpers.enum_field(1)
    instruments: List["InfoInstrument"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class InfoInstrument(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class SubscribeInfoResponse(grpc_helpers.Message):
    tracking_id: str = grpc_helpers.string_field(1)
    info_subscriptions: List["InfoSubscription"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class InfoSubscription(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    subscription_status: "SubscriptionStatus" = grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class Candle(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    interval: "SubscriptionInterval" = grpc_helpers.enum_field(2)
    open: "Quotation" = grpc_helpers.message_field(3)
    high: "Quotation" = grpc_helpers.message_field(4)
    low: "Quotation" = grpc_helpers.message_field(5)
    close: "Quotation" = grpc_helpers.message_field(6)
    value: int = grpc_helpers.int64_field(7)
    time: datetime = grpc_helpers.message_field(8)


@dataclass(eq=False, repr=True)
class OrderBook(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    depth: int = grpc_helpers.int32_field(2)
    is_consistent: bool = grpc_helpers.bool_field(3)
    bids: List["Order"] = grpc_helpers.message_field(4)
    asks: List["Order"] = grpc_helpers.message_field(5)
    time: datetime = grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class Order(grpc_helpers.Message):
    price: "Quotation" = grpc_helpers.message_field(1)
    quantity: int = grpc_helpers.int64_field(2)


@dataclass(eq=False, repr=True)
class Trade(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    direction: "TradeDirection" = grpc_helpers.enum_field(2)
    price: "Quotation" = grpc_helpers.message_field(3)
    quantity: int = grpc_helpers.int64_field(4)
    timestamp: datetime = grpc_helpers.message_field(5)


@dataclass(eq=False, repr=True)
class TradingStatus(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    trading_status: "SecurityTradingStatus" = grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class GetCandlesRequest(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    from_: datetime = grpc_helpers.message_field(2)
    to: datetime = grpc_helpers.message_field(3)
    interval: "CandleInterval" = grpc_helpers.enum_field(4)


@dataclass(eq=False, repr=True)
class GetCandlesResponse(grpc_helpers.Message):
    candles: List["HistoricCandle"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class HistoricCandle(grpc_helpers.Message):
    open: "Quotation" = grpc_helpers.message_field(1)
    high: "Quotation" = grpc_helpers.message_field(2)
    low: "Quotation" = grpc_helpers.message_field(3)
    close: "Quotation" = grpc_helpers.message_field(4)
    volume: int = grpc_helpers.int64_field(5)
    time: datetime = grpc_helpers.message_field(6)
    is_complete: bool = grpc_helpers.bool_field(7)


@dataclass(eq=False, repr=True)
class GetLastPricesRequest(grpc_helpers.Message):
    figi: List[str] = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetLastPricesResponse(grpc_helpers.Message):
    last_prices: List["LastPrice"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class LastPrice(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    price: "Quotation" = grpc_helpers.message_field(2)
    time: datetime = grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class GetOrderBookRequest(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    depth: int = grpc_helpers.int32_field(2)


@dataclass(eq=False, repr=True)
class GetOrderBookResponse(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    depth: int = grpc_helpers.int32_field(2)
    bids: List["Order"] = grpc_helpers.message_field(3)
    asks: List["Order"] = grpc_helpers.message_field(4)
    last_price: "Quotation" = grpc_helpers.message_field(5)
    close_price: "Quotation" = grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class GetTradingStatusRequest(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetTradingStatusResponse(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    trading_status: "SecurityTradingStatus" = grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class OperationsRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)
    from_: datetime = grpc_helpers.message_field(2)
    to: datetime = grpc_helpers.message_field(3)
    state: "OperationState" = grpc_helpers.enum_field(4)
    figi: str = grpc_helpers.string_field(5)


@dataclass(eq=False, repr=True)
class OperationsResponse(grpc_helpers.Message):
    operations: List["Operation"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Operation(grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    id: str = grpc_helpers.string_field(1)
    parent_operation_id: str = grpc_helpers.string_field(2)
    currency: str = grpc_helpers.string_field(3)
    payment: "MoneyValue" = grpc_helpers.message_field(4)
    price: "MoneyValue" = grpc_helpers.message_field(5)
    state: "OperationState" = grpc_helpers.enum_field(6)
    quantity: int = grpc_helpers.int64_field(7)
    quantity_rest: int = grpc_helpers.int64_field(8)
    figi: str = grpc_helpers.string_field(9)
    instrument_type: str = grpc_helpers.string_field(10)
    date: datetime = grpc_helpers.message_field(11)
    type: str = grpc_helpers.string_field(12)


@dataclass(eq=False, repr=True)
class PortfolioRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class PortfolioResponse(grpc_helpers.Message):
    total_amount_shares: "MoneyValue" = grpc_helpers.message_field(1)
    total_amount_bonds: "MoneyValue" = grpc_helpers.message_field(2)
    total_amount_etf: "MoneyValue" = grpc_helpers.message_field(3)
    total_amount_currencies: "MoneyValue" = grpc_helpers.message_field(4)
    total_amount_futures: "MoneyValue" = grpc_helpers.message_field(5)
    expected_yield: Decimal = grpc_helpers.float_field(6)
    positions: List["PortfolioPosition"] = grpc_helpers.message_field(7)


@dataclass(eq=False, repr=True)
class PositionsRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class PositionsResponse(grpc_helpers.Message):
    money: List["MoneyValue"] = grpc_helpers.message_field(1)
    blocked: List["MoneyValue"] = grpc_helpers.message_field(2)
    securities: List["PositionsSecurities"] = grpc_helpers.message_field(3)
    limits_loading_in_progress: bool = grpc_helpers.bool_field(4)


@dataclass(eq=False, repr=True)
class WithdrawLimitsRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class WithdrawLimitsResponse(grpc_helpers.Message):
    money: List["MoneyValue"] = grpc_helpers.message_field(1)
    blocked: List["MoneyValue"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class PortfolioPosition(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    instrument_type: str = grpc_helpers.string_field(2)
    quantity: Decimal = grpc_helpers.float_field(3)
    average_position_price: "MoneyValue" = grpc_helpers.message_field(4)
    expected_yield: Decimal = grpc_helpers.float_field(5)
    current_nkd: "MoneyValue" = grpc_helpers.message_field(6)
    average_position_price_pt: "Quotation" = grpc_helpers.message_field(7)


@dataclass(eq=False, repr=True)
class PositionsSecurities(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    blocked: int = grpc_helpers.int64_field(2)
    balance: int = grpc_helpers.int64_field(3)


@dataclass(eq=False, repr=True)
class TradesStreamRequest(grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class TradesStreamResponse(grpc_helpers.Message):
    order_id: str = grpc_helpers.string_field(1)
    created_at: datetime = grpc_helpers.message_field(2)
    direction: "OrderDirection" = grpc_helpers.enum_field(3)
    figi: str = grpc_helpers.string_field(4)
    trades: List["OrderTrade"] = grpc_helpers.message_field(5)


@dataclass(eq=False, repr=True)
class OrderTrade(grpc_helpers.Message):
    date_time: datetime = grpc_helpers.message_field(1)
    price: "Quotation" = grpc_helpers.message_field(2)
    quantity: int = grpc_helpers.int64_field(3)


@dataclass(eq=False, repr=True)
class PostOrderRequest(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    quantity: int = grpc_helpers.int64_field(2)
    price: "Quotation" = grpc_helpers.message_field(3)
    direction: "OrderDirection" = grpc_helpers.enum_field(4)
    account_id: str = grpc_helpers.string_field(5)
    order_type: "OrderType" = grpc_helpers.enum_field(6)
    order_id: str = grpc_helpers.string_field(7)


@dataclass(eq=False, repr=True)
class PostOrderResponse(  # pylint:disable=too-many-instance-attributes
    grpc_helpers.Message
):
    order_id: str = grpc_helpers.string_field(1)
    execution_report_status: "OrderExecutionReportStatus" = grpc_helpers.enum_field(2)
    lots_requested: int = grpc_helpers.int64_field(3)
    lots_executed: int = grpc_helpers.int64_field(4)
    initial_order_price: "MoneyValue" = grpc_helpers.message_field(5)
    executed_order_price: "MoneyValue" = grpc_helpers.message_field(6)
    total_order_amount: "MoneyValue" = grpc_helpers.message_field(7)
    initial_commission: "MoneyValue" = grpc_helpers.message_field(8)
    executed_commission: "MoneyValue" = grpc_helpers.message_field(9)
    aci_value: "MoneyValue" = grpc_helpers.message_field(10)
    figi: str = grpc_helpers.string_field(11)
    direction: "OrderDirection" = grpc_helpers.enum_field(12)
    initial_security_price: "MoneyValue" = grpc_helpers.message_field(13)
    order_type: "OrderType" = grpc_helpers.enum_field(14)
    message: str = grpc_helpers.string_field(15)
    initial_order_price_pt: "Quotation" = grpc_helpers.message_field(16)


@dataclass(eq=False, repr=True)
class CancelOrderRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)
    order_id: str = grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class CancelOrderResponse(grpc_helpers.Message):
    time: datetime = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class GetOrderStateRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)
    order_id: str = grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class GetOrdersRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetOrdersResponse(grpc_helpers.Message):
    orders: List["OrderState"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class OrderState(grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    order_id: str = grpc_helpers.string_field(1)
    execution_report_status: "OrderExecutionReportStatus" = grpc_helpers.enum_field(2)
    lots_requested: int = grpc_helpers.int64_field(3)
    lots_executed: int = grpc_helpers.int64_field(4)
    initial_order_price: "MoneyValue" = grpc_helpers.message_field(5)
    executed_order_price: "MoneyValue" = grpc_helpers.message_field(6)
    total_order_amount: "MoneyValue" = grpc_helpers.message_field(7)
    average_position_price: "MoneyValue" = grpc_helpers.message_field(8)
    initial_commission: "MoneyValue" = grpc_helpers.message_field(9)
    executed_commission: "MoneyValue" = grpc_helpers.message_field(10)
    figi: str = grpc_helpers.string_field(11)
    direction: "OrderDirection" = grpc_helpers.enum_field(12)
    initial_security_price: "MoneyValue" = grpc_helpers.message_field(13)
    stages: List["OrderStage"] = grpc_helpers.message_field(14)
    service_commission: "MoneyValue" = grpc_helpers.message_field(15)
    currency: str = grpc_helpers.string_field(16)
    order_type: "OrderType" = grpc_helpers.enum_field(17)
    order_date: datetime = grpc_helpers.message_field(18)


@dataclass(eq=False, repr=True)
class OrderStage(grpc_helpers.Message):
    price: "MoneyValue" = grpc_helpers.message_field(1)
    quantity: int = grpc_helpers.int64_field(2)
    trade_id: str = grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class GetAccountsRequest(grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetAccountsResponse(grpc_helpers.Message):
    accounts: List["Account"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Account(grpc_helpers.Message):
    id: str = grpc_helpers.string_field(1)
    type: "AccountType" = grpc_helpers.enum_field(2)
    name: str = grpc_helpers.string_field(3)
    status: "AccountStatus" = grpc_helpers.enum_field(4)
    opened_date: datetime = grpc_helpers.message_field(5)
    closed_date: datetime = grpc_helpers.message_field(6)

    @classmethod
    def loads(cls, obj) -> "Account":
        return cls(
            id=obj.id,
            type=AccountType(obj.type),
            name=obj.name,
            status=AccountStatus(obj.type),
            opened_date=grpc_helpers.ts_to_datetime(obj.opened_date),
            closed_date=grpc_helpers.ts_to_datetime(obj.closed_date),
        )


@dataclass(eq=False, repr=True)
class GetMarginAttributesRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetMarginAttributesResponse(grpc_helpers.Message):
    liquid_portfolio: "MoneyValue" = grpc_helpers.message_field(1)
    starting_margin: "MoneyValue" = grpc_helpers.message_field(2)
    minimal_margin: "MoneyValue" = grpc_helpers.message_field(3)
    funds_sufficiency_level: "Quotation" = grpc_helpers.message_field(4)
    amount_of_missing_funds: "MoneyValue" = grpc_helpers.message_field(5)


@dataclass(eq=False, repr=True)
class GetUserTariffRequest(grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetUserTariffResponse(grpc_helpers.Message):
    unary_limits: List["UnaryLimit"] = grpc_helpers.message_field(1)
    stream_limits: List["StreamLimit"] = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class UnaryLimit(grpc_helpers.Message):
    limit_per_minute: int = grpc_helpers.int32_field(1)
    methods: List[str] = grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class StreamLimit(grpc_helpers.Message):
    limit: int = grpc_helpers.int32_field(1)
    streams: List[str] = grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class GetInfoRequest(grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetInfoResponse(grpc_helpers.Message):
    prem_status: bool = grpc_helpers.bool_field(1)
    qual_status: bool = grpc_helpers.bool_field(2)
    qualified_for_work_with: List[str] = grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class OpenSandboxAccountRequest(grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class OpenSandboxAccountResponse(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class CloseSandboxAccountRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class CloseSandboxAccountResponse(grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class SandboxPayInRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)
    amount: "MoneyValue" = grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class SandboxPayInResponse(grpc_helpers.Message):
    balance: "MoneyValue" = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class PostStopOrderRequest(grpc_helpers.Message):
    figi: str = grpc_helpers.string_field(1)
    quantity: int = grpc_helpers.int64_field(2)
    price: "Quotation" = grpc_helpers.message_field(3)
    stop_price: "Quotation" = grpc_helpers.message_field(4)
    direction: "StopOrderDirection" = grpc_helpers.enum_field(5)
    account_id: str = grpc_helpers.string_field(6)
    expiration_type: "StopOrderExpirationType" = grpc_helpers.enum_field(7)
    stop_order_type: "StopOrderType" = grpc_helpers.enum_field(8)
    expire_date: datetime = grpc_helpers.message_field(9)


@dataclass(eq=False, repr=True)
class PostStopOrderResponse(grpc_helpers.Message):
    stop_order_id: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetStopOrdersRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetStopOrdersResponse(grpc_helpers.Message):
    stop_orders: List["StopOrder"] = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class CancelStopOrderRequest(grpc_helpers.Message):
    account_id: str = grpc_helpers.string_field(1)
    stop_order_id: str = grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class CancelStopOrderResponse(grpc_helpers.Message):
    time: datetime = grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class StopOrder(grpc_helpers.Message):
    stop_order_id: str = grpc_helpers.string_field(1)
    lots_requested: int = grpc_helpers.int64_field(2)
    figi: str = grpc_helpers.string_field(3)
    direction: "StopOrderDirection" = grpc_helpers.enum_field(4)
    currency: str = grpc_helpers.string_field(5)
    order_type: "StopOrderType" = grpc_helpers.enum_field(6)
    create_date: datetime = grpc_helpers.message_field(7)
    activation_date_time: datetime = grpc_helpers.message_field(8)
    expiration_time: datetime = grpc_helpers.message_field(9)
