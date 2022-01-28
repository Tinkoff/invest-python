# pylint:disable=too-many-lines
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

from . import _grpc_helpers


class SecurityTradingStatus(_grpc_helpers.Enum):
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
    SECURITY_TRADING_STATUS_SESSION_ASSIGNED = 11
    SECURITY_TRADING_STATUS_SESSION_CLOSE = 12
    SECURITY_TRADING_STATUS_SESSION_OPEN = 13
    SECURITY_TRADING_STATUS_DEALER_NORMAL_TRADING = 14
    SECURITY_TRADING_STATUS_DEALER_BREAK_IN_TRADING = 15
    SECURITY_TRADING_STATUS_DEALER_NOT_AVAILABLE_FOR_TRADING = 16


class InstrumentIdType(_grpc_helpers.Enum):
    INSTRUMENT_ID_UNSPECIFIED = 0
    INSTRUMENT_ID_TYPE_FIGI = 1
    INSTRUMENT_ID_TYPE_TICKER = 2


class InstrumentStatus(_grpc_helpers.Enum):
    INSTRUMENT_STATUS_UNSPECIFIED = 0
    INSTRUMENT_STATUS_BASE = 1
    INSTRUMENT_STATUS_ALL = 2


class ShareType(_grpc_helpers.Enum):
    SHARE_TYPE_UNSPECIFIED = 0
    SHARE_TYPE_COMMON = 1
    SHARE_TYPE_PREFERRED = 2
    SHARE_TYPE_ADR = 3
    SHARE_TYPE_GDR = 4
    SHARE_TYPE_MLP = 5
    SHARE_TYPE_NY_REG_SHRS = 6
    SHARE_TYPE_CLOSED_END_FUND = 7
    SHARE_TYPE_REIT = 8


class SubscriptionAction(_grpc_helpers.Enum):
    SUBSCRIPTION_ACTION_UNSPECIFIED = 0
    SUBSCRIPTION_ACTION_SUBSCRIBE = 1
    SUBSCRIPTION_ACTION_UNSUBSCRIBE = 2


class SubscriptionInterval(_grpc_helpers.Enum):
    SUBSCRIPTION_INTERVAL_UNSPECIFIED = 0
    SUBSCRIPTION_INTERVAL_ONE_MINUTE = 1
    SUBSCRIPTION_INTERVAL_FIVE_MINUTES = 2


class SubscriptionStatus(_grpc_helpers.Enum):
    SUBSCRIPTION_STATUS_UNSPECIFIED = 0
    SUBSCRIPTION_STATUS_SUCCESS = 1
    SUBSCRIPTION_STATUS_INSTRUMENT_NOT_FOUND = 2
    SUBSCRIPTION_STATUS_SUBSCRIPTION_ACTION_IS_INVALID = 3
    SUBSCRIPTION_STATUS_DEPTH_IS_INVALID = 4
    SUBSCRIPTION_STATUS_INTERVAL_IS_INVALID = 5
    SUBSCRIPTION_STATUS_LIMIT_IS_EXCEEDED = 6
    SUBSCRIPTION_STATUS_INTERNAL_ERROR = 7


class TradeDirection(_grpc_helpers.Enum):
    TRADE_DIRECTION_UNSPECIFIED = 0
    TRADE_DIRECTION_BUY = 1
    TRADE_DIRECTION_SELL = 2


class CandleInterval(_grpc_helpers.Enum):
    CANDLE_INTERVAL_UNSPECIFIED = 0
    CANDLE_INTERVAL_1_MIN = 1
    CANDLE_INTERVAL_5_MIN = 2
    CANDLE_INTERVAL_15_MIN = 3
    CANDLE_INTERVAL_HOUR = 4
    CANDLE_INTERVAL_DAY = 5


class OperationState(_grpc_helpers.Enum):
    OPERATION_STATE_UNSPECIFIED = 0
    OPERATION_STATE_EXECUTED = 1
    OPERATION_STATE_CANCELED = 2


class OrderDirection(_grpc_helpers.Enum):
    ORDER_DIRECTION_UNSPECIFIED = 0
    ORDER_DIRECTION_BUY = 1
    ORDER_DIRECTION_SELL = 2


class OrderType(_grpc_helpers.Enum):
    ORDER_TYPE_UNSPECIFIED = 0
    ORDER_TYPE_LIMIT = 1
    ORDER_TYPE_MARKET = 2


class OrderExecutionReportStatus(_grpc_helpers.Enum):
    EXECUTION_REPORT_STATUS_UNSPECIFIED = 0
    EXECUTION_REPORT_STATUS_FILL = 1
    EXECUTION_REPORT_STATUS_REJECTED = 2
    EXECUTION_REPORT_STATUS_CANCELLED = 3
    EXECUTION_REPORT_STATUS_NEW = 4
    EXECUTION_REPORT_STATUS_PARTIALLYFILL = 5


class AccountType(_grpc_helpers.Enum):
    ACCOUNT_TYPE_UNSPECIFIED = 0
    ACCOUNT_TYPE_TINKOFF = 1
    ACCOUNT_TYPE_TINKOFF_IIS = 2
    ACCOUNT_TYPE_INVEST_BOX = 3


class AccountStatus(_grpc_helpers.Enum):
    ACCOUNT_STATUS_UNSPECIFIED = 0
    ACCOUNT_STATUS_NEW = 1
    ACCOUNT_STATUS_OPEN = 2
    ACCOUNT_STATUS_CLOSED = 3


class StopOrderDirection(_grpc_helpers.Enum):
    STOP_ORDER_DIRECTION_UNSPECIFIED = 0
    STOP_ORDER_DIRECTION_BUY = 1
    STOP_ORDER_DIRECTION_SELL = 2


class StopOrderExpirationType(_grpc_helpers.Enum):
    STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED = 0
    STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL = 1
    STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_DATE = 2


class StopOrderType(_grpc_helpers.Enum):
    STOP_ORDER_TYPE_UNSPECIFIED = 0
    STOP_ORDER_TYPE_TAKE_PROFIT = 1
    STOP_ORDER_TYPE_STOP_LOSS = 2
    STOP_ORDER_TYPE_STOP_LIMIT = 3


class OperationType(_grpc_helpers.Enum):
    OPERATION_TYPE_UNSPECIFIED = 0
    OPERATION_TYPE_INPUT = 1
    OPERATION_TYPE_BOND_TAX = 2
    OPERATION_TYPE_OUTPUT_SECURITIES = 3
    OPERATION_TYPE_OVERNIGHT = 4
    OPERATION_TYPE_TAX = 5
    OPERATION_TYPE_BOND_REPAYMENT_FULL = 6
    OPERATION_TYPE_SELL_CARD = 7
    OPERATION_TYPE_DIVIDEND_TAX = 8
    OPERATION_TYPE_OUTPUT = 9
    OPERATION_TYPE_BOND_REPAYMENT = 10
    OPERATION_TYPE_TAX_CORRECTION = 11
    OPERATION_TYPE_SERVICE_FEE = 12
    OPERATION_TYPE_BENEFIT_TAX = 13
    OPERATION_TYPE_MARGIN_FEE = 14
    OPERATION_TYPE_BUY = 15
    OPERATION_TYPE_BUY_CARD = 16
    OPERATION_TYPE_INPUT_SECURITIES = 17
    OPERATION_TYPE_SELL_MARJIN = 18
    OPERATION_TYPE_BROKER_FEE = 19
    OPERATION_TYPE_BUY_MARGIN = 20
    OPERATION_TYPE_DIVIDEND = 21
    OPERATION_TYPE_SELL = 22
    OPERATION_TYPE_COUPON = 23
    OPERATION_TYPE_SUCCESS_FEE = 24
    OPERATION_TYPE_DIVIDEND_TRANSFER = 25
    OPERATION_TYPE_ACCRUING_VARMARJIN = 26
    OPERATION_TYPE_WRITING_OFF_VARMARJIN = 27
    OPERATION_TYPE_DELIVERY_BUY = 28
    OPERATION_TYPE_DELIVERY_SELL = 29
    OPERATION_TYPE_TRACK_MFEE = 30
    OPERATION_TYPE_TRACK_PFEE = 31
    OPERATION_TYPE_TAX_PROGRESSIVE = 32
    OPERATION_TYPE_BOND_TAX_PROGRESSIVE = 33
    OPERATION_TYPE_DIVIDEND_TAX_PROGRESSIVE = 34
    OPERATION_TYPE_BENEFIT_TAX_PROGRESSIVE = 35
    OPERATION_TYPE_TAX_CORRECTION_PROGRESSIVE = 36
    OPERATION_TYPE_TAX_REPO_PROGRESSIVE = 37
    OPERATION_TYPE_TAX_REPO = 38
    OPERATION_TYPE_TAX_REPO_HOLD = 39
    OPERATION_TYPE_TAX_REPO_REFUND = 40
    OPERATION_TYPE_TAX_REPO_HOLD_PROGRESSIVE = 41
    OPERATION_TYPE_TAX_REPO_REFUND_PROGRESSIVE = 42
    OPERATION_TYPE_DIV_EXT = 43


@dataclass(eq=False, repr=True)
class MoneyValue(_grpc_helpers.Message):
    currency: str = _grpc_helpers.string_field(1)
    units: int = _grpc_helpers.int64_field(2)
    nano: int = _grpc_helpers.int32_field(3)


@dataclass(eq=False, repr=True)
class Quotation(_grpc_helpers.Message):
    units: int = _grpc_helpers.int64_field(1)
    nano: int = _grpc_helpers.int32_field(2)


@dataclass(eq=False, repr=True)
class Ping(_grpc_helpers.Message):
    time: datetime = _grpc_helpers.int64_field(1)


@dataclass(eq=False, repr=True)
class TradingSchedulesRequest(_grpc_helpers.Message):
    exchange: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class TradingSchedulesResponse(_grpc_helpers.Message):
    exchanges: List["TradingSchedule"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class TradingSchedule(_grpc_helpers.Message):
    exchange: str = _grpc_helpers.string_field(1)
    days: List["TradingDay"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class TradingDay(_grpc_helpers.Message):
    date: datetime = _grpc_helpers.message_field(1)
    is_trading_day: bool = _grpc_helpers.bool_field(2)
    start_time: datetime = _grpc_helpers.message_field(3)
    end_time: datetime = _grpc_helpers.message_field(4)
    market_order_start_time: datetime = _grpc_helpers.message_field(5)
    market_order_end_time: datetime = _grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class InstrumentRequest(_grpc_helpers.Message):
    id_type: "InstrumentIdType" = _grpc_helpers.enum_field(1)
    class_code: str = _grpc_helpers.string_field(2)
    id: str = _grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class InstrumentsRequest(_grpc_helpers.Message):
    instrument_status: "InstrumentStatus" = _grpc_helpers.enum_field(1)


@dataclass(eq=False, repr=True)
class BondResponse(_grpc_helpers.Message):
    instrument: "Bond" = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class BondsResponse(_grpc_helpers.Message):
    instruments: List["Bond"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class CurrencyResponse(_grpc_helpers.Message):
    instrument: "Currency" = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class CurrenciesResponse(_grpc_helpers.Message):
    instruments: List["Currency"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class EtfResponse(_grpc_helpers.Message):
    instrument: "Etf" = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class EtfsResponse(_grpc_helpers.Message):
    instruments: List["Etf"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class FutureResponse(_grpc_helpers.Message):
    instrument: "Future" = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class FuturesResponse(_grpc_helpers.Message):
    instruments: List["Future"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class ShareResponse(_grpc_helpers.Message):
    instrument: "Share" = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class SharesResponse(_grpc_helpers.Message):
    instruments: List["Share"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Bond(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    lot: int = _grpc_helpers.int32_field(5)
    currency: str = _grpc_helpers.string_field(6)
    klong: Decimal = _grpc_helpers.double_field(7)
    kshort: Decimal = _grpc_helpers.double_field(8)
    dlong: Decimal = _grpc_helpers.double_field(9)
    dshort: Decimal = _grpc_helpers.double_field(10)
    dlong_min: Decimal = _grpc_helpers.double_field(11)
    dshort_min: Decimal = _grpc_helpers.double_field(12)
    short_enabled_flag: bool = _grpc_helpers.bool_field(13)
    name: str = _grpc_helpers.string_field(15)
    exchange: str = _grpc_helpers.string_field(16)
    coupon_quantity_per_year: int = _grpc_helpers.int32_field(17)
    maturity_date: datetime = _grpc_helpers.message_field(18)
    nominal: "MoneyValue" = _grpc_helpers.message_field(19)
    state_reg_date: datetime = _grpc_helpers.message_field(21)
    placement_date: datetime = _grpc_helpers.message_field(22)
    placement_price: "MoneyValue" = _grpc_helpers.message_field(23)
    aci_value: "MoneyValue" = _grpc_helpers.message_field(24)
    country_of_risk: str = _grpc_helpers.string_field(25)
    country_of_risk_name: str = _grpc_helpers.string_field(26)
    sector: str = _grpc_helpers.string_field(27)
    issue_kind: str = _grpc_helpers.string_field(28)
    issue_size: int = _grpc_helpers.int64_field(29)
    issue_size_plan: int = _grpc_helpers.int64_field(30)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(31)
    otc_flag: bool = _grpc_helpers.bool_field(32)
    buy_available_flag: bool = _grpc_helpers.bool_field(33)
    sell_available_flag: bool = _grpc_helpers.bool_field(34)
    floating_coupon_flag: bool = _grpc_helpers.bool_field(35)
    perpetual_flag: bool = _grpc_helpers.bool_field(36)
    amortization_flag: bool = _grpc_helpers.bool_field(37)
    min_price_increment: Decimal = _grpc_helpers.float_field(38)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(39)


@dataclass(eq=False, repr=True)
class Currency(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    lot: int = _grpc_helpers.int32_field(5)
    currency: str = _grpc_helpers.string_field(6)
    klong: Decimal = _grpc_helpers.double_field(7)
    kshort: Decimal = _grpc_helpers.double_field(8)
    dlong: Decimal = _grpc_helpers.double_field(9)
    dshort: Decimal = _grpc_helpers.double_field(10)
    dlong_min: Decimal = _grpc_helpers.double_field(11)
    dshort_min: Decimal = _grpc_helpers.double_field(12)
    short_enabled_flag: bool = _grpc_helpers.bool_field(13)
    name: str = _grpc_helpers.string_field(15)
    exchange: str = _grpc_helpers.string_field(16)
    nominal: "MoneyValue" = _grpc_helpers.message_field(17)
    country_of_risk: str = _grpc_helpers.string_field(18)
    country_of_risk_name: str = _grpc_helpers.string_field(19)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(20)
    otc_flag: bool = _grpc_helpers.bool_field(21)
    buy_available_flag: bool = _grpc_helpers.bool_field(22)
    sell_available_flag: bool = _grpc_helpers.bool_field(23)
    iso_currency_name: str = _grpc_helpers.string_field(24)
    min_price_increment: Decimal = _grpc_helpers.float_field(25)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(26)


@dataclass(eq=False, repr=True)
class Etf(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    lot: int = _grpc_helpers.int32_field(5)
    currency: str = _grpc_helpers.string_field(6)
    klong: Decimal = _grpc_helpers.double_field(7)
    kshort: Decimal = _grpc_helpers.double_field(8)
    dlong: Decimal = _grpc_helpers.double_field(9)
    dshort: Decimal = _grpc_helpers.double_field(10)
    dlong_min: Decimal = _grpc_helpers.double_field(11)
    dshort_min: Decimal = _grpc_helpers.double_field(12)
    short_enabled_flag: bool = _grpc_helpers.bool_field(13)
    name: str = _grpc_helpers.string_field(15)
    exchange: str = _grpc_helpers.string_field(16)
    fixed_commission: Decimal = _grpc_helpers.double_field(17)
    focus_type: str = _grpc_helpers.string_field(18)
    released_date: datetime = _grpc_helpers.message_field(19)
    num_shares: Decimal = _grpc_helpers.double_field(20)
    country_of_risk: str = _grpc_helpers.string_field(21)
    country_of_risk_name: str = _grpc_helpers.string_field(22)
    sector: str = _grpc_helpers.string_field(23)
    rebalancing_freq: str = _grpc_helpers.string_field(24)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(25)
    otc_flag: bool = _grpc_helpers.bool_field(26)
    buy_available_flag: bool = _grpc_helpers.bool_field(27)
    sell_available_flag: bool = _grpc_helpers.bool_field(28)
    min_price_increment: Decimal = _grpc_helpers.float_field(29)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(30)


@dataclass(eq=False, repr=True)
class Future(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    lot: int = _grpc_helpers.int32_field(4)
    currency: str = _grpc_helpers.string_field(5)
    klong: Decimal = _grpc_helpers.double_field(6)
    kshort: Decimal = _grpc_helpers.double_field(7)
    dlong: Decimal = _grpc_helpers.double_field(8)
    dshort: Decimal = _grpc_helpers.double_field(9)
    dlong_min: Decimal = _grpc_helpers.double_field(10)
    dshort_min: Decimal = _grpc_helpers.double_field(11)
    short_enabled_flag: bool = _grpc_helpers.bool_field(12)
    name: str = _grpc_helpers.string_field(13)
    exchange: str = _grpc_helpers.string_field(14)
    first_trade_date: datetime = _grpc_helpers.message_field(15)
    last_trade_date: datetime = _grpc_helpers.message_field(16)
    futures_type: str = _grpc_helpers.string_field(17)
    asset_type: str = _grpc_helpers.string_field(18)
    basic_asset: str = _grpc_helpers.string_field(19)
    basic_asset_size: Decimal = _grpc_helpers.double_field(20)
    country_of_risk: str = _grpc_helpers.string_field(21)
    country_of_risk_name: str = _grpc_helpers.string_field(22)
    sector: str = _grpc_helpers.string_field(23)
    expiration_date: datetime = _grpc_helpers.message_field(24)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(25)
    otc_flag: bool = _grpc_helpers.bool_field(26)
    buy_available_flag: bool = _grpc_helpers.bool_field(27)
    sell_available_flag: bool = _grpc_helpers.bool_field(28)
    min_price_increment: Decimal = _grpc_helpers.float_field(29)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(30)


@dataclass(eq=False, repr=True)
class Share(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    lot: int = _grpc_helpers.int32_field(5)
    currency: str = _grpc_helpers.string_field(6)
    klong: Decimal = _grpc_helpers.double_field(7)
    kshort: Decimal = _grpc_helpers.double_field(8)
    dlong: Decimal = _grpc_helpers.double_field(9)
    dshort: Decimal = _grpc_helpers.double_field(10)
    dlong_min: Decimal = _grpc_helpers.double_field(11)
    dshort_min: Decimal = _grpc_helpers.double_field(12)
    short_enabled_flag: bool = _grpc_helpers.bool_field(13)
    name: str = _grpc_helpers.string_field(15)
    exchange: str = _grpc_helpers.string_field(16)
    ipo_date: datetime = _grpc_helpers.message_field(17)
    issue_size: int = _grpc_helpers.int64_field(18)
    country_of_risk: str = _grpc_helpers.string_field(19)
    country_of_risk_name: str = _grpc_helpers.string_field(20)
    sector: str = _grpc_helpers.string_field(21)
    issue_size_plan: int = _grpc_helpers.int64_field(22)
    nominal: "MoneyValue" = _grpc_helpers.message_field(23)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(25)
    otc_flag: bool = _grpc_helpers.bool_field(26)
    buy_available_flag: bool = _grpc_helpers.bool_field(27)
    sell_available_flag: bool = _grpc_helpers.bool_field(28)
    div_yield_flag: bool = _grpc_helpers.bool_field(29)
    share_type: "ShareType" = _grpc_helpers.enum_field(30)
    min_price_increment: Decimal = _grpc_helpers.float_field(31)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(32)


@dataclass(eq=False, repr=True)
class GetAccruedInterestsRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class GetAccruedInterestsResponse(_grpc_helpers.Message):
    accrued_interests: List["AccruedInterest"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class AccruedInterest(_grpc_helpers.Message):
    date: datetime = _grpc_helpers.message_field(1)
    value: "Quotation" = _grpc_helpers.message_field(2)
    value_percent: Decimal = _grpc_helpers.float_field(3)
    nominal: "Quotation" = _grpc_helpers.message_field(4)


@dataclass(eq=False, repr=True)
class GetFuturesMarginRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetFuturesMarginResponse(_grpc_helpers.Message):
    initial_margin_on_buy: "MoneyValue" = _grpc_helpers.message_field(1)
    initial_margin_on_sell: "MoneyValue" = _grpc_helpers.message_field(2)
    min_price_increment: Decimal = _grpc_helpers.message_field(3)
    min_price_increment_amount: "Quotation" = _grpc_helpers.message_field(4)


@dataclass(eq=False, repr=True)
class InstrumentResponse(_grpc_helpers.Message):
    instrument: "Instrument" = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Instrument(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    lot: int = _grpc_helpers.int32_field(5)
    currency: str = _grpc_helpers.string_field(6)
    klong: Decimal = _grpc_helpers.double_field(7)
    kshort: Decimal = _grpc_helpers.double_field(8)
    dlong: Decimal = _grpc_helpers.double_field(9)
    dshort: Decimal = _grpc_helpers.double_field(10)
    dlong_min: Decimal = _grpc_helpers.double_field(11)
    dshort_min: Decimal = _grpc_helpers.double_field(12)
    short_enabled_flag: bool = _grpc_helpers.bool_field(13)
    name: str = _grpc_helpers.string_field(14)
    exchange: str = _grpc_helpers.string_field(15)
    country_of_risk: str = _grpc_helpers.string_field(16)
    country_of_risk_name: str = _grpc_helpers.string_field(17)
    instrument_type: str = _grpc_helpers.string_field(18)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(19)
    otc_flag: bool = _grpc_helpers.bool_field(20)
    buy_available_flag: bool = _grpc_helpers.bool_field(21)
    sell_available_flag: bool = _grpc_helpers.bool_field(22)
    min_price_increment: Decimal = _grpc_helpers.float_field(23)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(24)


@dataclass(eq=False, repr=True)
class GetDividendsRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class GetDividendsResponse(_grpc_helpers.Message):
    dividends: List["Dividend"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Dividend(_grpc_helpers.Message):
    dividend_net: "MoneyValue" = _grpc_helpers.message_field(1)
    payment_date: datetime = _grpc_helpers.message_field(2)
    declared_date: datetime = _grpc_helpers.message_field(3)
    last_buy_date: datetime = _grpc_helpers.message_field(4)
    dividend_type: str = _grpc_helpers.string_field(5)
    record_date: datetime = _grpc_helpers.message_field(6)
    regularity: str = _grpc_helpers.string_field(7)
    close_price: "MoneyValue" = _grpc_helpers.message_field(8)
    yield_value: "Quotation" = _grpc_helpers.message_field(9)
    created_at: datetime = _grpc_helpers.message_field(10)


@dataclass(eq=False, repr=True)
class MarketDataRequest(_grpc_helpers.Message):
    subscribe_candles_request: "SubscribeCandlesRequest" = _grpc_helpers.message_field(
        1, group="payload"
    )
    subscribe_order_book_request: "SubscribeOrderBookRequest" = (
        _grpc_helpers.message_field(2, group="payload")
    )
    subscribe_trades_request: "SubscribeTradesRequest" = _grpc_helpers.message_field(
        3, group="payload"
    )
    subscribe_info_request: "SubscribeInfoRequest" = _grpc_helpers.message_field(
        4, group="payload"
    )


@dataclass(eq=False, repr=True)
class MarketDataResponse(_grpc_helpers.Message):
    subscribe_candles_response: "SubscribeCandlesResponse" = (
        _grpc_helpers.message_field(1, group="payload")
    )
    subscribe_order_book_response: "SubscribeOrderBookResponse" = (
        _grpc_helpers.message_field(2, group="payload")
    )
    subscribe_trades_response: "SubscribeTradesResponse" = _grpc_helpers.message_field(
        3, group="payload"
    )
    subscribe_info_response: "SubscribeInfoResponse" = _grpc_helpers.message_field(
        4, group="payload"
    )
    candle: "Candle" = _grpc_helpers.message_field(5, group="payload")
    trade: "Trade" = _grpc_helpers.message_field(6, group="payload")
    orderbook: "OrderBook" = _grpc_helpers.message_field(7, group="payload")
    trading_status: "TradingStatus" = _grpc_helpers.message_field(8, group="payload")
    ping: "Ping" = _grpc_helpers.message_field(9, group="payload")


@dataclass(eq=False, repr=True)
class SubscribeCandlesRequest(_grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = _grpc_helpers.enum_field(1)
    instruments: List["CandleInstrument"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class CandleInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    interval: "SubscriptionInterval" = _grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class SubscribeCandlesResponse(_grpc_helpers.Message):
    tracking_id: str = _grpc_helpers.string_field(1)
    candles_subscriptions: List["CandleSubscription"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class CandleSubscription(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    interval: "SubscriptionInterval" = _grpc_helpers.enum_field(2)
    subscription_status: "SubscriptionStatus" = _grpc_helpers.enum_field(3)


@dataclass(eq=False, repr=True)
class SubscribeOrderBookRequest(_grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = _grpc_helpers.enum_field(1)
    instruments: List["OrderBookInstrument"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class OrderBookInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    depth: int = _grpc_helpers.int32_field(2)


@dataclass(eq=False, repr=True)
class SubscribeOrderBookResponse(_grpc_helpers.Message):
    tracking_id: str = _grpc_helpers.string_field(1)
    order_book_subscriptions: List[
        "OrderBookSubscription"
    ] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class OrderBookSubscription(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    depth: int = _grpc_helpers.int32_field(2)
    subscription_status: "SubscriptionStatus" = _grpc_helpers.enum_field(3)


@dataclass(eq=False, repr=True)
class SubscribeTradesRequest(_grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = _grpc_helpers.enum_field(1)
    instruments: List["TradeInstrument"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class TradeInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class SubscribeTradesResponse(_grpc_helpers.Message):
    tracking_id: str = _grpc_helpers.string_field(1)
    trade_subscriptions: List["TradeSubscription"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class TradeSubscription(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    subscription_status: "SubscriptionStatus" = _grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class SubscribeInfoRequest(_grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = _grpc_helpers.enum_field(1)
    instruments: List["InfoInstrument"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class InfoInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class SubscribeInfoResponse(_grpc_helpers.Message):
    tracking_id: str = _grpc_helpers.string_field(1)
    info_subscriptions: List["InfoSubscription"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class InfoSubscription(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    subscription_status: "SubscriptionStatus" = _grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class Candle(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    interval: "SubscriptionInterval" = _grpc_helpers.enum_field(2)
    open: "Quotation" = _grpc_helpers.message_field(3)
    high: "Quotation" = _grpc_helpers.message_field(4)
    low: "Quotation" = _grpc_helpers.message_field(5)
    close: "Quotation" = _grpc_helpers.message_field(6)
    volume: int = _grpc_helpers.int64_field(7)
    time: datetime = _grpc_helpers.message_field(8)


@dataclass(eq=False, repr=True)
class OrderBook(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    depth: int = _grpc_helpers.int32_field(2)
    is_consistent: bool = _grpc_helpers.bool_field(3)
    bids: List["Order"] = _grpc_helpers.message_field(4)
    asks: List["Order"] = _grpc_helpers.message_field(5)
    time: datetime = _grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class Order(_grpc_helpers.Message):
    price: "Quotation" = _grpc_helpers.message_field(1)
    quantity: int = _grpc_helpers.int64_field(2)


@dataclass(eq=False, repr=True)
class Trade(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    direction: "TradeDirection" = _grpc_helpers.enum_field(2)
    price: "Quotation" = _grpc_helpers.message_field(3)
    quantity: int = _grpc_helpers.int64_field(4)
    time: datetime = _grpc_helpers.message_field(5)


@dataclass(eq=False, repr=True)
class TradingStatus(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(2)
    time: datetime = _grpc_helpers.enum_field(3)


@dataclass(eq=False, repr=True)
class GetCandlesRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)
    interval: "CandleInterval" = _grpc_helpers.enum_field(4)


@dataclass(eq=False, repr=True)
class GetCandlesResponse(_grpc_helpers.Message):
    candles: List["HistoricCandle"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class HistoricCandle(_grpc_helpers.Message):
    open: "Quotation" = _grpc_helpers.message_field(1)
    high: "Quotation" = _grpc_helpers.message_field(2)
    low: "Quotation" = _grpc_helpers.message_field(3)
    close: "Quotation" = _grpc_helpers.message_field(4)
    volume: int = _grpc_helpers.int64_field(5)
    time: datetime = _grpc_helpers.message_field(6)
    is_complete: bool = _grpc_helpers.bool_field(7)


@dataclass(eq=False, repr=True)
class GetLastPricesRequest(_grpc_helpers.Message):
    figi: List[str] = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetLastPricesResponse(_grpc_helpers.Message):
    last_prices: List["LastPrice"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class LastPrice(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    price: "Quotation" = _grpc_helpers.message_field(2)
    time: datetime = _grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class GetOrderBookRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    depth: int = _grpc_helpers.int32_field(2)


@dataclass(eq=False, repr=True)
class GetOrderBookResponse(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    depth: int = _grpc_helpers.int32_field(2)
    bids: List["Order"] = _grpc_helpers.message_field(3)
    asks: List["Order"] = _grpc_helpers.message_field(4)
    last_price: "Quotation" = _grpc_helpers.message_field(5)
    close_price: "Quotation" = _grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class GetTradingStatusRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetTradingStatusResponse(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class OperationsRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)
    state: "OperationState" = _grpc_helpers.enum_field(4)
    figi: str = _grpc_helpers.string_field(5)


@dataclass(eq=False, repr=True)
class OperationsResponse(_grpc_helpers.Message):
    operations: List["Operation"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Operation(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    id: str = _grpc_helpers.string_field(1)
    parent_operation_id: str = _grpc_helpers.string_field(2)
    currency: str = _grpc_helpers.string_field(3)
    payment: "MoneyValue" = _grpc_helpers.message_field(4)
    price: "MoneyValue" = _grpc_helpers.message_field(5)
    state: "OperationState" = _grpc_helpers.enum_field(6)
    quantity: int = _grpc_helpers.int64_field(7)
    quantity_rest: int = _grpc_helpers.int64_field(8)
    figi: str = _grpc_helpers.string_field(9)
    instrument_type: str = _grpc_helpers.string_field(10)
    date: datetime = _grpc_helpers.message_field(11)
    type: str = _grpc_helpers.string_field(12)
    operation_type: "OperationType" = _grpc_helpers.string_field(13)


@dataclass(eq=False, repr=True)
class PortfolioRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class PortfolioResponse(_grpc_helpers.Message):
    total_amount_shares: "MoneyValue" = _grpc_helpers.message_field(1)
    total_amount_bonds: "MoneyValue" = _grpc_helpers.message_field(2)
    total_amount_etf: "MoneyValue" = _grpc_helpers.message_field(3)
    total_amount_currencies: "MoneyValue" = _grpc_helpers.message_field(4)
    total_amount_futures: "MoneyValue" = _grpc_helpers.message_field(5)
    expected_yield: Decimal = _grpc_helpers.float_field(6)
    positions: List["PortfolioPosition"] = _grpc_helpers.message_field(7)


@dataclass(eq=False, repr=True)
class PositionsRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class PositionsResponse(_grpc_helpers.Message):
    money: List["MoneyValue"] = _grpc_helpers.message_field(1)
    blocked: List["MoneyValue"] = _grpc_helpers.message_field(2)
    securities: List["PositionsSecurities"] = _grpc_helpers.message_field(3)
    limits_loading_in_progress: bool = _grpc_helpers.bool_field(4)


@dataclass(eq=False, repr=True)
class WithdrawLimitsRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class WithdrawLimitsResponse(_grpc_helpers.Message):
    money: List["MoneyValue"] = _grpc_helpers.message_field(1)
    blocked: List["MoneyValue"] = _grpc_helpers.message_field(2)
    blocked_guarantee: List["MoneyValue"] = _grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class PortfolioPosition(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    instrument_type: str = _grpc_helpers.string_field(2)
    quantity: Decimal = _grpc_helpers.float_field(3)
    average_position_price: "MoneyValue" = _grpc_helpers.message_field(4)
    expected_yield: Decimal = _grpc_helpers.float_field(5)
    current_nkd: "MoneyValue" = _grpc_helpers.message_field(6)
    average_position_price_pt: "Quotation" = _grpc_helpers.message_field(7)


@dataclass(eq=False, repr=True)
class PositionsSecurities(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    blocked: int = _grpc_helpers.int64_field(2)
    balance: int = _grpc_helpers.int64_field(3)


@dataclass(eq=False, repr=True)
class TradesStreamRequest(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class TradesStreamResponse(_grpc_helpers.Message):
    order_trades: "OrderTrades" = _grpc_helpers.message_field(1, group="payload")
    ping: "Ping" = _grpc_helpers.message_field(2, group="payload")


@dataclass(eq=False, repr=True)
class OrderTrades(_grpc_helpers.Message):
    order_id: str = _grpc_helpers.string_field(1)
    created_at: datetime = _grpc_helpers.message_field(2)
    direction: "OrderDirection" = _grpc_helpers.enum_field(3)
    figi: str = _grpc_helpers.string_field(4)
    trades: List["OrderTrade"] = _grpc_helpers.message_field(5)


@dataclass(eq=False, repr=True)
class OrderTrade(_grpc_helpers.Message):
    date_time: datetime = _grpc_helpers.message_field(1)
    price: "Quotation" = _grpc_helpers.message_field(2)
    quantity: int = _grpc_helpers.int64_field(3)


@dataclass(eq=False, repr=True)
class PostOrderRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    quantity: int = _grpc_helpers.int64_field(2)
    price: "Quotation" = _grpc_helpers.message_field(3)
    direction: "OrderDirection" = _grpc_helpers.enum_field(4)
    account_id: str = _grpc_helpers.string_field(5)
    order_type: "OrderType" = _grpc_helpers.enum_field(6)
    order_id: str = _grpc_helpers.string_field(7)


@dataclass(eq=False, repr=True)
class PostOrderResponse(  # pylint:disable=too-many-instance-attributes
    _grpc_helpers.Message
):
    order_id: str = _grpc_helpers.string_field(1)
    execution_report_status: "OrderExecutionReportStatus" = _grpc_helpers.enum_field(2)
    lots_requested: int = _grpc_helpers.int64_field(3)
    lots_executed: int = _grpc_helpers.int64_field(4)
    initial_order_price: "MoneyValue" = _grpc_helpers.message_field(5)
    executed_order_price: "MoneyValue" = _grpc_helpers.message_field(6)
    total_order_amount: "MoneyValue" = _grpc_helpers.message_field(7)
    initial_commission: "MoneyValue" = _grpc_helpers.message_field(8)
    executed_commission: "MoneyValue" = _grpc_helpers.message_field(9)
    aci_value: "MoneyValue" = _grpc_helpers.message_field(10)
    figi: str = _grpc_helpers.string_field(11)
    direction: "OrderDirection" = _grpc_helpers.enum_field(12)
    initial_security_price: "MoneyValue" = _grpc_helpers.message_field(13)
    order_type: "OrderType" = _grpc_helpers.enum_field(14)
    message: str = _grpc_helpers.string_field(15)
    initial_order_price_pt: "Quotation" = _grpc_helpers.message_field(16)


@dataclass(eq=False, repr=True)
class CancelOrderRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    order_id: str = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class CancelOrderResponse(_grpc_helpers.Message):
    time: datetime = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class GetOrderStateRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    order_id: str = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class GetOrdersRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetOrdersResponse(_grpc_helpers.Message):
    orders: List["OrderState"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class OrderState(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    order_id: str = _grpc_helpers.string_field(1)
    execution_report_status: "OrderExecutionReportStatus" = _grpc_helpers.enum_field(2)
    lots_requested: int = _grpc_helpers.int64_field(3)
    lots_executed: int = _grpc_helpers.int64_field(4)
    initial_order_price: "MoneyValue" = _grpc_helpers.message_field(5)
    executed_order_price: "MoneyValue" = _grpc_helpers.message_field(6)
    total_order_amount: "MoneyValue" = _grpc_helpers.message_field(7)
    average_position_price: "MoneyValue" = _grpc_helpers.message_field(8)
    initial_commission: "MoneyValue" = _grpc_helpers.message_field(9)
    executed_commission: "MoneyValue" = _grpc_helpers.message_field(10)
    figi: str = _grpc_helpers.string_field(11)
    direction: "OrderDirection" = _grpc_helpers.enum_field(12)
    initial_security_price: "MoneyValue" = _grpc_helpers.message_field(13)
    stages: List["OrderStage"] = _grpc_helpers.message_field(14)
    service_commission: "MoneyValue" = _grpc_helpers.message_field(15)
    currency: str = _grpc_helpers.string_field(16)
    order_type: "OrderType" = _grpc_helpers.enum_field(17)
    order_date: datetime = _grpc_helpers.message_field(18)


@dataclass(eq=False, repr=True)
class OrderStage(_grpc_helpers.Message):
    price: "MoneyValue" = _grpc_helpers.message_field(1)
    quantity: int = _grpc_helpers.int64_field(2)
    trade_id: str = _grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class GetAccountsRequest(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetAccountsResponse(_grpc_helpers.Message):
    accounts: List["Account"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Account(_grpc_helpers.Message):
    id: str = _grpc_helpers.string_field(1)
    type: "AccountType" = _grpc_helpers.enum_field(2)
    name: str = _grpc_helpers.string_field(3)
    status: "AccountStatus" = _grpc_helpers.enum_field(4)
    opened_date: datetime = _grpc_helpers.message_field(5)
    closed_date: datetime = _grpc_helpers.message_field(6)

    @classmethod
    def loads(cls, obj) -> "Account":
        return cls(
            id=obj.id,
            type=AccountType(obj.type),
            name=obj.name,
            status=AccountStatus(obj.type),
            opened_date=_grpc_helpers.ts_to_datetime(obj.opened_date),
            closed_date=_grpc_helpers.ts_to_datetime(obj.closed_date),
        )


@dataclass(eq=False, repr=True)
class GetMarginAttributesRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetMarginAttributesResponse(_grpc_helpers.Message):
    liquid_portfolio: "MoneyValue" = _grpc_helpers.message_field(1)
    starting_margin: "MoneyValue" = _grpc_helpers.message_field(2)
    minimal_margin: "MoneyValue" = _grpc_helpers.message_field(3)
    funds_sufficiency_level: "Quotation" = _grpc_helpers.message_field(4)
    amount_of_missing_funds: "MoneyValue" = _grpc_helpers.message_field(5)


@dataclass(eq=False, repr=True)
class GetUserTariffRequest(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetUserTariffResponse(_grpc_helpers.Message):
    unary_limits: List["UnaryLimit"] = _grpc_helpers.message_field(1)
    stream_limits: List["StreamLimit"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class UnaryLimit(_grpc_helpers.Message):
    limit_per_minute: int = _grpc_helpers.int32_field(1)
    methods: List[str] = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class StreamLimit(_grpc_helpers.Message):
    limit: int = _grpc_helpers.int32_field(1)
    streams: List[str] = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class GetInfoRequest(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetInfoResponse(_grpc_helpers.Message):
    prem_status: bool = _grpc_helpers.bool_field(1)
    qual_status: bool = _grpc_helpers.bool_field(2)
    qualified_for_work_with: List[str] = _grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class OpenSandboxAccountRequest(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class OpenSandboxAccountResponse(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class CloseSandboxAccountRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class CloseSandboxAccountResponse(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class SandboxPayInRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    amount: "MoneyValue" = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class SandboxPayInResponse(_grpc_helpers.Message):
    balance: "MoneyValue" = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class PostStopOrderRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    quantity: int = _grpc_helpers.int64_field(2)
    price: "Quotation" = _grpc_helpers.message_field(3)
    stop_price: "Quotation" = _grpc_helpers.message_field(4)
    direction: "StopOrderDirection" = _grpc_helpers.enum_field(5)
    account_id: str = _grpc_helpers.string_field(6)
    expiration_type: "StopOrderExpirationType" = _grpc_helpers.enum_field(7)
    stop_order_type: "StopOrderType" = _grpc_helpers.enum_field(8)
    expire_date: datetime = _grpc_helpers.message_field(9)


@dataclass(eq=False, repr=True)
class PostStopOrderResponse(_grpc_helpers.Message):
    stop_order_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetStopOrdersRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetStopOrdersResponse(_grpc_helpers.Message):
    stop_orders: List["StopOrder"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class CancelStopOrderRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    stop_order_id: str = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class CancelStopOrderResponse(_grpc_helpers.Message):
    time: datetime = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class StopOrder(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    stop_order_id: str = _grpc_helpers.string_field(1)
    lots_requested: int = _grpc_helpers.int64_field(2)
    figi: str = _grpc_helpers.string_field(3)
    direction: "StopOrderDirection" = _grpc_helpers.enum_field(4)
    currency: str = _grpc_helpers.string_field(5)
    order_type: "StopOrderType" = _grpc_helpers.enum_field(6)
    create_date: datetime = _grpc_helpers.message_field(7)
    activation_date_time: datetime = _grpc_helpers.message_field(8)
    expiration_time: datetime = _grpc_helpers.message_field(9)
    price: "MoneyValue" = _grpc_helpers.message_field(10)
    stop_price: "MoneyValue" = _grpc_helpers.message_field(11)


@dataclass(eq=False, repr=True)
class BrokerReportRequest(_grpc_helpers.Message):
    generate_broker_report_request: "GenerateBrokerReportRequest" = (
        _grpc_helpers.message_field(1, group="payload")
    )
    get_broker_report_request: "GetBrokerReportRequest" = _grpc_helpers.message_field(
        2, group="payload"
    )


@dataclass(eq=False, repr=True)
class BrokerReportResponse(_grpc_helpers.Message):
    generate_broker_report_response: "GenerateBrokerReportResponse" = (
        _grpc_helpers.message_field(1, group="payload")
    )
    get_broker_report_response: "GetBrokerReportResponse" = _grpc_helpers.message_field(
        2, group="payload"
    )


@dataclass(eq=False, repr=True)
class GenerateBrokerReportRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class GenerateBrokerReportResponse(_grpc_helpers.Message):
    task_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetBrokerReportRequest(_grpc_helpers.Message):
    task_id: str = _grpc_helpers.string_field(1)
    page: int = _grpc_helpers.int32_field(2)


@dataclass(eq=False, repr=True)
class GetBrokerReportResponse(_grpc_helpers.Message):
    broker_report: List["BrokerReport"] = _grpc_helpers.message_field(1)
    itemsCount: int = _grpc_helpers.int32_field(2)
    pagesCount: int = _grpc_helpers.int32_field(3)
    page: int = _grpc_helpers.int32_field(4)


@dataclass(eq=False, repr=True)
class BrokerReport(  # pylint:disable=too-many-instance-attributes
    _grpc_helpers.Message
):
    trade_id: str = _grpc_helpers.string_field(1)
    order_id: str = _grpc_helpers.string_field(2)
    figi: str = _grpc_helpers.string_field(3)
    execute_sign: str = _grpc_helpers.string_field(4)
    trade_datetime: datetime = _grpc_helpers.message_field(5)
    exchange: str = _grpc_helpers.string_field(6)
    class_code: str = _grpc_helpers.string_field(7)
    direction: str = _grpc_helpers.string_field(8)
    name: str = _grpc_helpers.string_field(9)
    ticker: str = _grpc_helpers.string_field(10)
    price: "MoneyValue" = _grpc_helpers.message_field(11)
    quantity: int = _grpc_helpers.int64_field(12)
    order_amount: "MoneyValue" = _grpc_helpers.message_field(13)
    aci_value: float = _grpc_helpers.double_field(14)
    total_order_amount: "MoneyValue" = _grpc_helpers.message_field(15)
    broker_commission: "MoneyValue" = _grpc_helpers.message_field(16)
    exchange_commission: "MoneyValue" = _grpc_helpers.message_field(17)
    exchange_clearing_commission: "MoneyValue" = _grpc_helpers.message_field(18)
    repo_rate: float = _grpc_helpers.double_field(19)
    party: str = _grpc_helpers.string_field(20)
    clear_value_date: datetime = _grpc_helpers.message_field(21)
    sec_value_date: datetime = _grpc_helpers.message_field(22)
    broker_status: str = _grpc_helpers.string_field(23)
    separate_agreement_type: str = _grpc_helpers.string_field(24)
    separate_agreement_number: str = _grpc_helpers.string_field(25)
    separate_agreement_date: str = _grpc_helpers.string_field(26)
    delivery_type: str = _grpc_helpers.string_field(27)
