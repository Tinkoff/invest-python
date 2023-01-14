# pylint:disable=too-many-lines
# pylint:disable=too-many-instance-attributes
from dataclasses import dataclass
from datetime import datetime
from typing import List, SupportsAbs

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
    INSTRUMENT_ID_TYPE_UID = 3
    INSTRUMENT_ID_TYPE_POSITION_UID = 4


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
    SUBSCRIPTION_STATUS_TOO_MANY_REQUESTS = 8


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
    OPERATION_STATE_PROGRESS = 3


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
    OPERATION_TYPE_SELL_MARGIN = 18
    OPERATION_TYPE_BROKER_FEE = 19
    OPERATION_TYPE_BUY_MARGIN = 20
    OPERATION_TYPE_DIVIDEND = 21
    OPERATION_TYPE_SELL = 22
    OPERATION_TYPE_COUPON = 23
    OPERATION_TYPE_SUCCESS_FEE = 24
    OPERATION_TYPE_DIVIDEND_TRANSFER = 25
    OPERATION_TYPE_ACCRUING_VARMARGIN = 26
    OPERATION_TYPE_WRITING_OFF_VARMARGIN = 27
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
    OPERATION_TYPE_TAX_CORRECTION_COUPON = 44
    OPERATION_TYPE_CASH_FEE = 45
    OPERATION_TYPE_OUT_FEE = 46
    OPERATION_TYPE_OUT_STAMP_DUTY = 47
    OPERATION_TYPE_OUTPUT_SWIFT = 50
    OPERATION_TYPE_INPUT_SWIFT = 51
    OPERATION_TYPE_OUTPUT_ACQUIRING = 53
    OPERATION_TYPE_INPUT_ACQUIRING = 54
    OPERATION_TYPE_OUTPUT_PENALTY = 55
    OPERATION_TYPE_ADVICE_FEE = 56
    OPERATION_TYPE_TRANS_IIS_BS = 57
    OPERATION_TYPE_TRANS_BS_BS = 58
    OPERATION_TYPE_OUT_MULTI = 59
    OPERATION_TYPE_INP_MULTI = 60
    OPERATION_TYPE_OVER_PLACEMENT = 61
    OPERATION_TYPE_OVER_COM = 62
    OPERATION_TYPE_OVER_INCOME = 63
    OPERATION_TYPE_OPTION_EXPIRATION = 64


class AccessLevel(_grpc_helpers.Enum):
    ACCOUNT_ACCESS_LEVEL_UNSPECIFIED = 0
    ACCOUNT_ACCESS_LEVEL_FULL_ACCESS = 1
    ACCOUNT_ACCESS_LEVEL_READ_ONLY = 2
    ACCOUNT_ACCESS_LEVEL_NO_ACCESS = 3


class CouponType(_grpc_helpers.Enum):
    COUPON_TYPE_UNSPECIFIED = 0
    COUPON_TYPE_CONSTANT = 1
    COUPON_TYPE_FLOATING = 2
    COUPON_TYPE_DISCOUNT = 3
    COUPON_TYPE_MORTGAGE = 4
    COUPON_TYPE_FIX = 5
    COUPON_TYPE_VARIABLE = 6
    COUPON_TYPE_OTHER = 7


class AssetType(_grpc_helpers.Enum):
    ASSET_TYPE_UNSPECIFIED = 0
    ASSET_TYPE_CURRENCY = 1
    ASSET_TYPE_COMMODITY = 2
    ASSET_TYPE_INDEX = 3
    ASSET_TYPE_SECURITY = 4


class StructuredProductType(_grpc_helpers.Enum):
    SP_TYPE_UNSPECIFIED = 0
    SP_TYPE_DELIVERABLE = 1
    SP_TYPE_NON_DELIVERABLE = 2


class EditFavoritesActionType(_grpc_helpers.Enum):
    EDIT_FAVORITES_ACTION_TYPE_UNSPECIFIED = 0
    EDIT_FAVORITES_ACTION_TYPE_ADD = 1
    EDIT_FAVORITES_ACTION_TYPE_DEL = 2


class RealExchange(_grpc_helpers.Enum):
    REAL_EXCHANGE_UNSPECIFIED = 0
    REAL_EXCHANGE_MOEX = 1
    REAL_EXCHANGE_RTS = 2
    REAL_EXCHANGE_OTC = 3


class PortfolioSubscriptionStatus(_grpc_helpers.Enum):
    PORTFOLIO_SUBSCRIPTION_STATUS_UNSPECIFIED = 0
    PORTFOLIO_SUBSCRIPTION_STATUS_SUCCESS = 1
    PORTFOLIO_SUBSCRIPTION_STATUS_ACCOUNT_NOT_FOUND = 2
    PORTFOLIO_SUBSCRIPTION_STATUS_INTERNAL_ERROR = 3


class InstrumentType(_grpc_helpers.Enum):
    INSTRUMENT_TYPE_UNSPECIFIED = 0
    INSTRUMENT_TYPE_BOND = 1
    INSTRUMENT_TYPE_SHARE = 2
    INSTRUMENT_TYPE_CURRENCY = 3
    INSTRUMENT_TYPE_ETF = 4
    INSTRUMENT_TYPE_FUTURES = 5
    INSTRUMENT_TYPE_SP = 6
    INSTRUMENT_TYPE_OPTION = 7


class PriceType(_grpc_helpers.Enum):
    PRICE_TYPE_UNSPECIFIED = 0
    PRICE_TYPE_POINT = 1
    PRICE_TYPE_CURRENCY = 2


class OptionDirection(_grpc_helpers.Enum):
    OPTION_DIRECTION_UNSPECIFIED = 0
    OPTION_DIRECTION_PUT = 1
    OPTION_DIRECTION_CALL = 2


class OptionPaymentType(_grpc_helpers.Enum):
    OPTION_PAYMENT_TYPE_UNSPECIFIED = 0
    OPTION_PAYMENT_TYPE_PREMIUM = 1
    OPTION_PAYMENT_TYPE_MARGINAL = 2


class OptionStyle(_grpc_helpers.Enum):
    OPTION_STYLE_UNSPECIFIED = 0
    OPTION_STYLE_AMERICAN = 1
    OPTION_STYLE_EUROPEAN = 2


class OptionSettlementType(_grpc_helpers.Enum):
    OPTION_EXECUTION_TYPE_UNSPECIFIED = 0
    OPTION_EXECUTION_TYPE_PHYSICAL_DELIVERY = 1
    OPTION_EXECUTION_TYPE_CASH_SETTLEMENT = 2


class PositionsAccountSubscriptionStatus(_grpc_helpers.Enum):
    POSITIONS_SUBSCRIPTION_STATUS_UNSPECIFIED = 0
    POSITIONS_SUBSCRIPTION_STATUS_SUCCESS = 1
    POSITIONS_SUBSCRIPTION_STATUS_ACCOUNT_NOT_FOUND = 2
    POSITIONS_SUBSCRIPTION_STATUS_INTERNAL_ERROR = 3


@dataclass(eq=False, repr=True)
class MoneyValue(_grpc_helpers.Message):
    currency: str = _grpc_helpers.string_field(1)
    units: int = _grpc_helpers.int64_field(2)
    nano: int = _grpc_helpers.int32_field(3)


@dataclass(eq=False, repr=True)
class Quotation(_grpc_helpers.Message, SupportsAbs):
    units: int = _grpc_helpers.int64_field(1)
    nano: int = _grpc_helpers.int32_field(2)

    def __init__(self, units: int, nano: int):
        max_quotation_nano = 1_000_000_000
        self.units = units + nano // max_quotation_nano
        self.nano = nano % max_quotation_nano

    def __add__(self, other: "Quotation") -> "Quotation":
        return Quotation(
            units=self.units + other.units,
            nano=self.nano + other.nano,
        )

    def __sub__(self, other: "Quotation") -> "Quotation":
        return Quotation(
            units=self.units - other.units,
            nano=self.nano - other.nano,
        )

    def __hash__(self) -> int:
        return hash((self.units, self.nano))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quotation):
            return NotImplemented
        return self.units == other.units and self.nano == other.nano

    def __lt__(self, other: "Quotation") -> bool:
        return self.units < other.units or (
            self.units == other.units and self.nano < other.nano
        )

    def __le__(self, other: "Quotation") -> bool:
        return self.units < other.units or (
            self.units == other.units and self.nano <= other.nano
        )

    def __gt__(self, other: "Quotation") -> bool:
        return self.units > other.units or (
            self.units == other.units and self.nano > other.nano
        )

    def __ge__(self, other: "Quotation") -> bool:
        return self.units > other.units or (
            self.units == other.units and self.nano >= other.nano
        )

    def __abs__(self) -> "Quotation":
        return Quotation(units=abs(self.units), nano=abs(self.nano))


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
class TradingDay(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    date: datetime = _grpc_helpers.message_field(1)
    is_trading_day: bool = _grpc_helpers.bool_field(2)
    start_time: datetime = _grpc_helpers.message_field(3)
    end_time: datetime = _grpc_helpers.message_field(4)
    # reserved 5,6
    opening_auction_start_time: datetime = _grpc_helpers.message_field(7)
    closing_auction_end_time: datetime = _grpc_helpers.message_field(8)
    evening_opening_auction_start_time: datetime = _grpc_helpers.message_field(9)
    evening_start_time: datetime = _grpc_helpers.message_field(10)
    evening_end_time: datetime = _grpc_helpers.message_field(11)
    clearing_start_time: datetime = _grpc_helpers.message_field(12)
    clearing_end_time: datetime = _grpc_helpers.message_field(13)
    premarket_start_time: datetime = _grpc_helpers.message_field(14)
    premarket_end_time: datetime = _grpc_helpers.message_field(15)


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
class GetBondCouponsRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class GetBondCouponsResponse(_grpc_helpers.Message):
    events: List["Coupon"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Coupon(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    coupon_date: datetime = _grpc_helpers.message_field(2)
    coupon_number: int = _grpc_helpers.int64_field(3)
    fix_date: datetime = _grpc_helpers.message_field(4)
    pay_one_bond: "MoneyValue" = _grpc_helpers.message_field(5)
    coupon_type: "CouponType" = _grpc_helpers.enum_field(6)
    coupon_start_date: datetime = _grpc_helpers.message_field(7)
    coupon_end_date: datetime = _grpc_helpers.message_field(8)
    coupon_period: int = _grpc_helpers.int32_field(9)


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
class OptionResponse(_grpc_helpers.Message):
    instrument: "Option" = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class OptionsResponse(_grpc_helpers.Message):
    instruments: List["Option"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class Option(_grpc_helpers.Message):
    uid: str = _grpc_helpers.string_field(1)
    position_uid: str = _grpc_helpers.string_field(2)
    ticker: str = _grpc_helpers.string_field(3)
    class_code: str = _grpc_helpers.string_field(4)
    basic_asset_position_uid: str = _grpc_helpers.string_field(5)

    trading_status: "SecurityTradingStatus" = _grpc_helpers.message_field(21)
    real_exchange: "RealExchange" = _grpc_helpers.message_field(31)
    direction: "OptionDirection" = _grpc_helpers.message_field(41)
    payment_type: "OptionPaymentType" = _grpc_helpers.message_field(42)
    style: "OptionStyle" = _grpc_helpers.message_field(43)
    settlement_type: "OptionSettlementType" = _grpc_helpers.message_field(44)

    name: str = _grpc_helpers.string_field(101)
    currency: str = _grpc_helpers.string_field(111)
    settlement_currency: str = _grpc_helpers.string_field(112)
    asset_type: str = _grpc_helpers.string_field(131)
    basic_asset: str = _grpc_helpers.string_field(132)
    exchange: str = _grpc_helpers.string_field(141)
    country_of_risk: str = _grpc_helpers.string_field(151)
    country_of_risk_name: str = _grpc_helpers.string_field(152)
    sector: str = _grpc_helpers.string_field(161)

    lot: int = _grpc_helpers.int32_field(201)
    basic_asset_size: "Quotation" = _grpc_helpers.message_field(211)
    klong: "Quotation" = _grpc_helpers.message_field(221)
    kshort: "Quotation" = _grpc_helpers.message_field(222)
    dlong: "Quotation" = _grpc_helpers.message_field(223)
    dshort: "Quotation" = _grpc_helpers.message_field(224)
    dlong_min: "Quotation" = _grpc_helpers.message_field(225)
    dshort_min: "Quotation" = _grpc_helpers.message_field(226)
    min_price_increment: "Quotation" = _grpc_helpers.message_field(231)
    strike_price: "MoneyValue" = _grpc_helpers.message_field(241)

    expiration_date: datetime = _grpc_helpers.message_field(301)
    first_trade_date: datetime = _grpc_helpers.message_field(311)
    last_trade_date: datetime = _grpc_helpers.message_field(312)
    first_1min_candle_date: datetime = _grpc_helpers.message_field(321)
    first_1day_candle_date: datetime = _grpc_helpers.message_field(322)

    short_enabled_flag: bool = _grpc_helpers.bool_field(401)
    for_iis_flag: bool = _grpc_helpers.bool_field(402)
    otc_flag: bool = _grpc_helpers.bool_field(403)
    buy_available_flag: bool = _grpc_helpers.bool_field(404)
    sell_available_flag: bool = _grpc_helpers.bool_field(405)
    for_qual_investor_flag: bool = _grpc_helpers.bool_field(406)
    weekend_flag: bool = _grpc_helpers.bool_field(407)
    blocked_tca_flag: bool = _grpc_helpers.bool_field(408)


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
    klong: "Quotation" = _grpc_helpers.message_field(7)
    kshort: "Quotation" = _grpc_helpers.message_field(8)
    dlong: "Quotation" = _grpc_helpers.message_field(9)
    dshort: "Quotation" = _grpc_helpers.message_field(10)
    dlong_min: "Quotation" = _grpc_helpers.message_field(11)
    dshort_min: "Quotation" = _grpc_helpers.message_field(12)
    short_enabled_flag: bool = _grpc_helpers.bool_field(13)
    name: str = _grpc_helpers.string_field(15)
    exchange: str = _grpc_helpers.string_field(16)
    coupon_quantity_per_year: int = _grpc_helpers.int32_field(17)
    maturity_date: datetime = _grpc_helpers.message_field(18)
    nominal: "MoneyValue" = _grpc_helpers.message_field(19)
    initial_nominal: "MoneyValue" = _grpc_helpers.message_field(20)
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
    min_price_increment: "Quotation" = _grpc_helpers.message_field(38)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(39)
    uid: str = _grpc_helpers.string_field(40)
    real_exchange: "RealExchange" = _grpc_helpers.message_field(41)
    position_uid: str = _grpc_helpers.string_field(42)
    for_iis_flag: bool = _grpc_helpers.bool_field(51)
    for_qual_investor_flag: bool = _grpc_helpers.bool_field(52)
    weekend_flag: bool = _grpc_helpers.bool_field(53)
    blocked_tca_flag: bool = _grpc_helpers.bool_field(54)
    first_1min_candle_date: datetime = _grpc_helpers.message_field(61)
    first_1day_candle_date: datetime = _grpc_helpers.message_field(62)


@dataclass(eq=False, repr=True)
class Currency(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    lot: int = _grpc_helpers.int32_field(5)
    currency: str = _grpc_helpers.string_field(6)
    klong: "Quotation" = _grpc_helpers.message_field(7)
    kshort: "Quotation" = _grpc_helpers.message_field(8)
    dlong: "Quotation" = _grpc_helpers.message_field(9)
    dshort: "Quotation" = _grpc_helpers.message_field(10)
    dlong_min: "Quotation" = _grpc_helpers.message_field(11)
    dshort_min: "Quotation" = _grpc_helpers.message_field(12)
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
    min_price_increment: "Quotation" = _grpc_helpers.message_field(25)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(26)
    uid: str = _grpc_helpers.string_field(27)
    real_exchange: "RealExchange" = _grpc_helpers.message_field(28)
    position_uid: str = _grpc_helpers.string_field(29)
    for_iis_flag: bool = _grpc_helpers.bool_field(41)
    for_qual_investor_flag: bool = _grpc_helpers.bool_field(52)
    weekend_flag: bool = _grpc_helpers.bool_field(53)
    blocked_tca_flag: bool = _grpc_helpers.bool_field(54)
    first_1min_candle_date: datetime = _grpc_helpers.message_field(56)
    first_1day_candle_date: datetime = _grpc_helpers.message_field(57)


@dataclass(eq=False, repr=True)
class Etf(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    lot: int = _grpc_helpers.int32_field(5)
    currency: str = _grpc_helpers.string_field(6)
    klong: "Quotation" = _grpc_helpers.message_field(7)
    kshort: "Quotation" = _grpc_helpers.message_field(8)
    dlong: "Quotation" = _grpc_helpers.message_field(9)
    dshort: "Quotation" = _grpc_helpers.message_field(10)
    dlong_min: "Quotation" = _grpc_helpers.message_field(11)
    dshort_min: "Quotation" = _grpc_helpers.message_field(12)
    short_enabled_flag: bool = _grpc_helpers.bool_field(13)
    name: str = _grpc_helpers.string_field(15)
    exchange: str = _grpc_helpers.string_field(16)
    fixed_commission: "Quotation" = _grpc_helpers.message_field(17)
    focus_type: str = _grpc_helpers.string_field(18)
    released_date: datetime = _grpc_helpers.message_field(19)
    num_shares: "Quotation" = _grpc_helpers.message_field(20)
    country_of_risk: str = _grpc_helpers.string_field(21)
    country_of_risk_name: str = _grpc_helpers.string_field(22)
    sector: str = _grpc_helpers.string_field(23)
    rebalancing_freq: str = _grpc_helpers.string_field(24)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(25)
    otc_flag: bool = _grpc_helpers.bool_field(26)
    buy_available_flag: bool = _grpc_helpers.bool_field(27)
    sell_available_flag: bool = _grpc_helpers.bool_field(28)
    min_price_increment: "Quotation" = _grpc_helpers.message_field(29)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(30)
    uid: str = _grpc_helpers.string_field(31)
    real_exchange: "RealExchange" = _grpc_helpers.message_field(32)
    position_uid: str = _grpc_helpers.string_field(33)
    for_iis_flag: bool = _grpc_helpers.bool_field(41)
    for_qual_investor_flag: bool = _grpc_helpers.bool_field(42)
    weekend_flag: bool = _grpc_helpers.bool_field(43)
    blocked_tca_flag: bool = _grpc_helpers.bool_field(44)
    first_1min_candle_date: datetime = _grpc_helpers.message_field(56)
    first_1day_candle_date: datetime = _grpc_helpers.message_field(57)


@dataclass(eq=False, repr=True)
class Future(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    lot: int = _grpc_helpers.int32_field(4)
    currency: str = _grpc_helpers.string_field(5)
    klong: "Quotation" = _grpc_helpers.message_field(6)
    kshort: "Quotation" = _grpc_helpers.message_field(7)
    dlong: "Quotation" = _grpc_helpers.message_field(8)
    dshort: "Quotation" = _grpc_helpers.message_field(9)
    dlong_min: "Quotation" = _grpc_helpers.message_field(10)
    dshort_min: "Quotation" = _grpc_helpers.message_field(11)
    short_enabled_flag: bool = _grpc_helpers.bool_field(12)
    name: str = _grpc_helpers.string_field(13)
    exchange: str = _grpc_helpers.string_field(14)
    first_trade_date: datetime = _grpc_helpers.message_field(15)
    last_trade_date: datetime = _grpc_helpers.message_field(16)
    futures_type: str = _grpc_helpers.string_field(17)
    asset_type: str = _grpc_helpers.string_field(18)
    basic_asset: str = _grpc_helpers.string_field(19)
    basic_asset_size: "Quotation" = _grpc_helpers.message_field(20)
    country_of_risk: str = _grpc_helpers.string_field(21)
    country_of_risk_name: str = _grpc_helpers.string_field(22)
    sector: str = _grpc_helpers.string_field(23)
    expiration_date: datetime = _grpc_helpers.message_field(24)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(25)
    otc_flag: bool = _grpc_helpers.bool_field(26)
    buy_available_flag: bool = _grpc_helpers.bool_field(27)
    sell_available_flag: bool = _grpc_helpers.bool_field(28)
    min_price_increment: "Quotation" = _grpc_helpers.message_field(29)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(30)
    uid: str = _grpc_helpers.string_field(31)
    real_exchange: "RealExchange" = _grpc_helpers.message_field(32)
    position_uid: str = _grpc_helpers.string_field(33)
    basic_asset_position_uid: str = _grpc_helpers.string_field(34)
    for_iis_flag: bool = _grpc_helpers.bool_field(41)
    for_qual_investor_flag: bool = _grpc_helpers.bool_field(42)
    weekend_flag: bool = _grpc_helpers.bool_field(43)
    blocked_tca_flag: bool = _grpc_helpers.bool_field(44)
    first_1min_candle_date: datetime = _grpc_helpers.message_field(56)
    first_1day_candle_date: datetime = _grpc_helpers.message_field(57)


@dataclass(eq=False, repr=True)
class Share(_grpc_helpers.Message):  # pylint:disable=too-many-instance-attributes
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    lot: int = _grpc_helpers.int32_field(5)
    currency: str = _grpc_helpers.string_field(6)
    klong: "Quotation" = _grpc_helpers.message_field(7)
    kshort: "Quotation" = _grpc_helpers.message_field(8)
    dlong: "Quotation" = _grpc_helpers.message_field(9)
    dshort: "Quotation" = _grpc_helpers.message_field(10)
    dlong_min: "Quotation" = _grpc_helpers.message_field(11)
    dshort_min: "Quotation" = _grpc_helpers.message_field(12)
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
    min_price_increment: "Quotation" = _grpc_helpers.message_field(31)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(32)
    uid: str = _grpc_helpers.string_field(33)
    real_exchange: "RealExchange" = _grpc_helpers.message_field(34)
    position_uid: str = _grpc_helpers.string_field(35)
    for_iis_flag: bool = _grpc_helpers.bool_field(46)
    for_qual_investor_flag: bool = _grpc_helpers.bool_field(47)
    weekend_flag: bool = _grpc_helpers.bool_field(48)
    blocked_tca_flag: bool = _grpc_helpers.bool_field(49)
    first_1min_candle_date: datetime = _grpc_helpers.message_field(56)
    first_1day_candle_date: datetime = _grpc_helpers.message_field(57)


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
    value_percent: "Quotation" = _grpc_helpers.message_field(3)
    nominal: "Quotation" = _grpc_helpers.message_field(4)


@dataclass(eq=False, repr=True)
class GetFuturesMarginRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetFuturesMarginResponse(_grpc_helpers.Message):
    initial_margin_on_buy: "MoneyValue" = _grpc_helpers.message_field(1)
    initial_margin_on_sell: "MoneyValue" = _grpc_helpers.message_field(2)
    min_price_increment: "Quotation" = _grpc_helpers.message_field(3)
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
    klong: "Quotation" = _grpc_helpers.message_field(7)
    kshort: "Quotation" = _grpc_helpers.message_field(8)
    dlong: "Quotation" = _grpc_helpers.message_field(9)
    dshort: "Quotation" = _grpc_helpers.message_field(10)
    dlong_min: "Quotation" = _grpc_helpers.message_field(11)
    dshort_min: "Quotation" = _grpc_helpers.message_field(12)
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
    min_price_increment: "Quotation" = _grpc_helpers.message_field(23)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(24)
    uid: str = _grpc_helpers.string_field(25)
    real_exchange: "RealExchange" = _grpc_helpers.message_field(26)
    position_uid: str = _grpc_helpers.string_field(27)
    for_iis_flag: bool = _grpc_helpers.bool_field(36)
    for_qual_investor_flag: bool = _grpc_helpers.bool_field(37)
    weekend_flag: bool = _grpc_helpers.bool_field(38)
    blocked_tca_flag: bool = _grpc_helpers.bool_field(39)
    first_1min_candle_date: datetime = _grpc_helpers.message_field(56)
    first_1day_candle_date: datetime = _grpc_helpers.message_field(57)


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
class AssetRequest(_grpc_helpers.Message):
    id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class AssetResponse(_grpc_helpers.Message):
    asset: "AssetFull" = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class AssetsRequest(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class AssetsResponse(_grpc_helpers.Message):
    assets: List["Asset"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class AssetFull(_grpc_helpers.Message):
    uid: str = _grpc_helpers.string_field(1)
    type: "AssetType" = _grpc_helpers.enum_field(2)
    name: str = _grpc_helpers.string_field(3)
    name_brief: str = _grpc_helpers.string_field(4)
    description: str = _grpc_helpers.string_field(5)
    deleted_at: datetime = _grpc_helpers.message_field(6)
    required_tests: List[str] = _grpc_helpers.message_field(7)
    currency: "AssetCurrency" = _grpc_helpers.message_field(8, group="ext")
    security: "AssetSecurity" = _grpc_helpers.message_field(9, group="ext")
    gos_reg_code: str = _grpc_helpers.string_field(10)
    cfi: str = _grpc_helpers.string_field(11)
    code_nsd: str = _grpc_helpers.string_field(12)
    status: str = _grpc_helpers.string_field(13)
    brand: "Brand" = _grpc_helpers.message_field(14)
    updated_at: datetime = _grpc_helpers.message_field(15)
    br_code: str = _grpc_helpers.string_field(16)
    br_code_name: str = _grpc_helpers.string_field(17)
    instruments: List["AssetInstrument"] = _grpc_helpers.message_field(18)


@dataclass(eq=False, repr=True)
class Asset(_grpc_helpers.Message):
    uid: str = _grpc_helpers.string_field(1)
    type: "AssetType" = _grpc_helpers.enum_field(2)
    name: str = _grpc_helpers.string_field(3)
    instruments: List["AssetInstrument"] = _grpc_helpers.message_field(4)


@dataclass(eq=False, repr=True)
class AssetCurrency(_grpc_helpers.Message):
    base_currency: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class AssetSecurity(_grpc_helpers.Message):
    isin: str = _grpc_helpers.string_field(1)
    type: str = _grpc_helpers.string_field(2)
    share: "AssetShare" = _grpc_helpers.message_field(3, group="ext")
    bond: "AssetBond" = _grpc_helpers.message_field(4, group="ext")
    sp: "AssetStructuredProduct" = _grpc_helpers.message_field(5, group="ext")
    etf: "AssetEtf" = _grpc_helpers.message_field(6, group="ext")
    clearing_certificate: "AssetClearingCertificate" = _grpc_helpers.message_field(
        7, group="ext"
    )


@dataclass(eq=False, repr=True)
class AssetShare(_grpc_helpers.Message):
    type: "ShareType" = _grpc_helpers.enum_field(1)
    issue_size: "Quotation" = _grpc_helpers.message_field(2)
    nominal: "Quotation" = _grpc_helpers.message_field(3)
    nominal_currency: str = _grpc_helpers.string_field(4)
    primary_index: str = _grpc_helpers.string_field(5)
    dividend_rate: "Quotation" = _grpc_helpers.message_field(6)
    preferred_share_type: str = _grpc_helpers.string_field(7)
    ipo_date: datetime = _grpc_helpers.message_field(8)
    registry_date: datetime = _grpc_helpers.message_field(9)
    div_yield_flag: bool = _grpc_helpers.bool_field(10)
    issue_kind: str = _grpc_helpers.string_field(11)
    placement_date: datetime = _grpc_helpers.message_field(12)
    repres_isin: str = _grpc_helpers.string_field(13)
    issue_size_plan: "Quotation" = _grpc_helpers.message_field(14)
    total_float: "Quotation" = _grpc_helpers.message_field(15)


@dataclass(eq=False, repr=True)
class AssetBond(_grpc_helpers.Message):
    current_nominal: "Quotation" = _grpc_helpers.message_field(1)
    borrow_name: str = _grpc_helpers.string_field(2)
    issue_size: "Quotation" = _grpc_helpers.message_field(3)
    nominal: "Quotation" = _grpc_helpers.message_field(4)
    nominal_currency: str = _grpc_helpers.string_field(5)
    issue_kind: str = _grpc_helpers.string_field(6)
    interest_kind: str = _grpc_helpers.string_field(7)
    coupon_quantity_per_year: int = _grpc_helpers.int32_field(8)
    indexed_nominal_flag: bool = _grpc_helpers.bool_field(9)
    subordinated_flag: bool = _grpc_helpers.bool_field(10)
    collateral_flag: bool = _grpc_helpers.bool_field(11)
    tax_free_flag: bool = _grpc_helpers.bool_field(12)
    amortization_flag: bool = _grpc_helpers.bool_field(13)
    floating_coupon_flag: bool = _grpc_helpers.bool_field(14)
    perpetual_flag: bool = _grpc_helpers.bool_field(15)
    maturity_date: datetime = _grpc_helpers.message_field(16)
    return_condition: str = _grpc_helpers.string_field(17)
    state_reg_date: datetime = _grpc_helpers.message_field(18)
    placement_date: datetime = _grpc_helpers.message_field(19)
    placement_price: "Quotation" = _grpc_helpers.message_field(20)
    issue_size_plan: "Quotation" = _grpc_helpers.message_field(21)


@dataclass(eq=False, repr=True)
class AssetStructuredProduct(_grpc_helpers.Message):
    borrow_name: str = _grpc_helpers.string_field(1)
    nominal: "Quotation" = _grpc_helpers.message_field(2)
    nominal_currency: str = _grpc_helpers.string_field(3)
    type: "StructuredProductType" = _grpc_helpers.enum_field(4)
    logic_portfolio: str = _grpc_helpers.string_field(5)
    asset_type: "AssetType" = _grpc_helpers.enum_field(6)
    basic_asset: str = _grpc_helpers.string_field(7)
    safety_barrier: "Quotation" = _grpc_helpers.message_field(8)
    maturity_date: datetime = _grpc_helpers.message_field(9)
    issue_size_plan: "Quotation" = _grpc_helpers.message_field(10)
    issue_size: "Quotation" = _grpc_helpers.message_field(11)
    placement_date: datetime = _grpc_helpers.message_field(12)
    issue_kind: str = _grpc_helpers.string_field(13)


@dataclass(eq=False, repr=True)
class AssetEtf(_grpc_helpers.Message):
    total_expense: "Quotation" = _grpc_helpers.message_field(1)
    hurdle_rate: "Quotation" = _grpc_helpers.message_field(2)
    performance_fee: "Quotation" = _grpc_helpers.message_field(3)
    fixed_commission: "Quotation" = _grpc_helpers.message_field(4)
    payment_type: str = _grpc_helpers.string_field(5)
    watermark_flag: bool = _grpc_helpers.bool_field(6)
    buy_premium: "Quotation" = _grpc_helpers.message_field(7)
    sell_discount: "Quotation" = _grpc_helpers.message_field(8)
    rebalancing_flag: bool = _grpc_helpers.bool_field(9)
    rebalancing_freq: str = _grpc_helpers.string_field(10)
    management_type: str = _grpc_helpers.string_field(11)
    primary_index: str = _grpc_helpers.string_field(12)
    focus_type: str = _grpc_helpers.string_field(13)
    leveraged_flag: bool = _grpc_helpers.bool_field(14)
    num_share: "Quotation" = _grpc_helpers.message_field(15)
    ucits_flag: bool = _grpc_helpers.bool_field(16)
    released_date: datetime = _grpc_helpers.message_field(17)
    description: str = _grpc_helpers.string_field(18)
    primary_index_description: str = _grpc_helpers.string_field(19)
    primary_index_company: str = _grpc_helpers.string_field(20)
    index_recovery_period: "Quotation" = _grpc_helpers.message_field(21)
    inav_code: str = _grpc_helpers.string_field(22)
    div_yield_flag: bool = _grpc_helpers.bool_field(23)
    expense_commission: "Quotation" = _grpc_helpers.message_field(24)
    primary_index_tracking_error: "Quotation" = _grpc_helpers.message_field(25)
    rebalancing_plan: str = _grpc_helpers.string_field(26)
    tax_rate: str = _grpc_helpers.string_field(27)
    rebalancing_dates: List[datetime] = _grpc_helpers.message_field(28)
    issue_kind: str = _grpc_helpers.string_field(29)
    nominal: "Quotation" = _grpc_helpers.message_field(30)
    nominal_currency: str = _grpc_helpers.string_field(31)


@dataclass(eq=False, repr=True)
class AssetClearingCertificate(_grpc_helpers.Message):
    nominal: "Quotation" = _grpc_helpers.message_field(1)
    nominal_currency: str = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class Brand(_grpc_helpers.Message):
    uid: str = _grpc_helpers.string_field(1)
    name: str = _grpc_helpers.string_field(2)
    description: str = _grpc_helpers.string_field(3)
    info: str = _grpc_helpers.string_field(4)
    company: str = _grpc_helpers.string_field(5)
    sector: str = _grpc_helpers.string_field(6)
    country_of_risk: str = _grpc_helpers.string_field(7)
    country_of_risk_name: str = _grpc_helpers.string_field(8)


@dataclass(eq=False, repr=True)
class AssetInstrument(_grpc_helpers.Message):
    uid: str = _grpc_helpers.string_field(1)
    figi: str = _grpc_helpers.string_field(2)
    instrument_type: str = _grpc_helpers.string_field(3)
    ticker: str = _grpc_helpers.string_field(4)
    class_code: str = _grpc_helpers.string_field(5)
    links: List["InstrumentLink"] = _grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class InstrumentLink(_grpc_helpers.Message):
    type: str = _grpc_helpers.string_field(1)
    instrument_uid: str = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class GetFavoritesRequest(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetFavoritesResponse(_grpc_helpers.Message):
    favorite_instruments: List["FavoriteInstrument"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class FavoriteInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    ticker: str = _grpc_helpers.string_field(2)
    class_code: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    instrument_type: str = _grpc_helpers.string_field(11)
    otc_flag: bool = _grpc_helpers.bool_field(16)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(17)


@dataclass(eq=False, repr=True)
class EditFavoritesRequest(_grpc_helpers.Message):
    instruments: List["EditFavoritesRequestInstrument"] = _grpc_helpers.message_field(1)
    action_type: "EditFavoritesActionType" = _grpc_helpers.enum_field(6)


@dataclass(eq=False, repr=True)
class EditFavoritesRequestInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class EditFavoritesResponse(_grpc_helpers.Message):
    favorite_instruments: List["FavoriteInstrument"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class GetCountriesRequest(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetCountriesResponse(_grpc_helpers.Message):
    countries: List["CountryResponse"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class CountryResponse(_grpc_helpers.Message):
    alfa_two: str = _grpc_helpers.string_field(1)
    alfa_three: str = _grpc_helpers.string_field(2)
    name: str = _grpc_helpers.string_field(3)
    name_brief: str = _grpc_helpers.string_field(4)


@dataclass(eq=False, repr=True)
class FindInstrumentRequest(_grpc_helpers.Message):
    query: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class FindInstrumentResponse(_grpc_helpers.Message):
    instruments: List["InstrumentShort"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class InstrumentShort(_grpc_helpers.Message):
    isin: str = _grpc_helpers.string_field(1)
    figi: str = _grpc_helpers.string_field(2)
    ticker: str = _grpc_helpers.string_field(3)
    class_code: str = _grpc_helpers.string_field(4)
    instrument_type: str = _grpc_helpers.string_field(5)
    name: str = _grpc_helpers.string_field(6)
    uid: str = _grpc_helpers.string_field(7)
    position_uid: str = _grpc_helpers.string_field(8)
    api_trade_available_flag: str = _grpc_helpers.string_field(11)
    for_iis_flag: bool = _grpc_helpers.bool_field(12)
    first_1min_candle_date: datetime = _grpc_helpers.message_field(26)
    first_1day_candle_date: datetime = _grpc_helpers.message_field(27)
    for_qual_investor_flag: bool = _grpc_helpers.bool_field(28)
    weekend_flag: bool = _grpc_helpers.bool_field(29)
    blocked_tca_flag: bool = _grpc_helpers.bool_field(30)


@dataclass(eq=False, repr=True)
class GetBrandsRequest(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetBrandRequest(_grpc_helpers.Message):
    id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetBrandsResponse(_grpc_helpers.Message):
    brands: List["Brand"] = _grpc_helpers.message_field(1)


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
    subscribe_last_price_request: "SubscribeLastPriceRequest" = (
        _grpc_helpers.message_field(5, group="payload")
    )
    get_my_subscriptions: "GetMySubscriptions" = _grpc_helpers.message_field(
        6, group="payload"
    )


@dataclass(eq=False, repr=True)
class MarketDataServerSideStreamRequest(_grpc_helpers.Message):
    subscribe_candles_request: "SubscribeCandlesRequest" = _grpc_helpers.message_field(
        1
    )
    subscribe_order_book_request: "SubscribeOrderBookRequest" = (
        _grpc_helpers.message_field(2)
    )
    subscribe_trades_request: "SubscribeTradesRequest" = _grpc_helpers.message_field(3)
    subscribe_info_request: "SubscribeInfoRequest" = _grpc_helpers.message_field(4)
    subscribe_last_price_request: "SubscribeLastPriceRequest" = (
        _grpc_helpers.message_field(5)
    )


@dataclass(eq=False, repr=True)
class MarketDataResponse(
    _grpc_helpers.Message
):  # pylint:disable=too-many-instance-attributes
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
    subscribe_last_price_response: "SubscribeLastPriceResponse" = (
        _grpc_helpers.message_field(10, group="payload")
    )
    last_price: "LastPrice" = _grpc_helpers.message_field(11, group="payload")


@dataclass(eq=False, repr=True)
class SubscribeCandlesRequest(_grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = _grpc_helpers.enum_field(1)
    instruments: List["CandleInstrument"] = _grpc_helpers.message_field(2)
    waiting_close: bool = _grpc_helpers.bool_field(3)


@dataclass(eq=False, repr=True)
class CandleInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    interval: "SubscriptionInterval" = _grpc_helpers.enum_field(2)
    instrument_id: str = _grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class SubscribeCandlesResponse(_grpc_helpers.Message):
    tracking_id: str = _grpc_helpers.string_field(1)
    candles_subscriptions: List["CandleSubscription"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class CandleSubscription(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    interval: "SubscriptionInterval" = _grpc_helpers.enum_field(2)
    subscription_status: "SubscriptionStatus" = _grpc_helpers.enum_field(3)
    instrument_uid: str = _grpc_helpers.string_field(4)


@dataclass(eq=False, repr=True)
class SubscribeOrderBookRequest(_grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = _grpc_helpers.enum_field(1)
    instruments: List["OrderBookInstrument"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class OrderBookInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    depth: int = _grpc_helpers.int32_field(2)
    instrument_id: str = _grpc_helpers.string_field(3)


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
    instrument_uid: str = _grpc_helpers.string_field(4)


@dataclass(eq=False, repr=True)
class SubscribeTradesRequest(_grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = _grpc_helpers.enum_field(1)
    instruments: List["TradeInstrument"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class SubscribeLastPriceRequest(_grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = _grpc_helpers.message_field(1)
    instruments: List["LastPriceInstrument"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class LastPriceInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    instrument_id: str = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class SubscribeLastPriceResponse(_grpc_helpers.Message):
    tracking_id: str = _grpc_helpers.string_field(1)
    last_price_subscriptions: List[
        "LastPriceSubscription"
    ] = _grpc_helpers.message_field(2)
    instrument_uid: str = _grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class LastPriceSubscription(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    subscription_status: "SubscriptionStatus" = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class TradeInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    instrument_id: str = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class SubscribeTradesResponse(_grpc_helpers.Message):
    tracking_id: str = _grpc_helpers.string_field(1)
    trade_subscriptions: List["TradeSubscription"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class TradeSubscription(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    subscription_status: "SubscriptionStatus" = _grpc_helpers.enum_field(2)
    instrument_uid: str = _grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class SubscribeInfoRequest(_grpc_helpers.Message):
    subscription_action: "SubscriptionAction" = _grpc_helpers.enum_field(1)
    instruments: List["InfoInstrument"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class InfoInstrument(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    instrument_uid: str = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class SubscribeInfoResponse(_grpc_helpers.Message):
    tracking_id: str = _grpc_helpers.string_field(1)
    info_subscriptions: List["InfoSubscription"] = _grpc_helpers.message_field(2)


@dataclass(eq=False, repr=True)
class InfoSubscription(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    subscription_status: "SubscriptionStatus" = _grpc_helpers.enum_field(2)
    instrument_uid: str = _grpc_helpers.string_field(3)


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
    last_trade_ts: datetime = _grpc_helpers.message_field(9)
    instrument_uid: str = _grpc_helpers.string_field(10)


@dataclass(eq=False, repr=True)
class OrderBook(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    depth: int = _grpc_helpers.int32_field(2)
    is_consistent: bool = _grpc_helpers.bool_field(3)
    bids: List["Order"] = _grpc_helpers.message_field(4)
    asks: List["Order"] = _grpc_helpers.message_field(5)
    time: datetime = _grpc_helpers.message_field(6)
    limit_up: "Quotation" = _grpc_helpers.message_field(7)
    limit_down: "Quotation" = _grpc_helpers.message_field(8)
    instrument_uid: str = _grpc_helpers.string_field(9)


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
    instrument_uid: str = _grpc_helpers.string_field(6)


@dataclass(eq=False, repr=True)
class TradingStatus(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(2)
    time: datetime = _grpc_helpers.enum_field(3)
    limit_order_available_flag: bool = _grpc_helpers.bool_field(4)
    market_order_available_flag: bool = _grpc_helpers.bool_field(5)
    instrument_uid: str = _grpc_helpers.string_field(6)


@dataclass(eq=False, repr=True)
class GetCandlesRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)
    interval: "CandleInterval" = _grpc_helpers.enum_field(4)
    instrument_id: str = _grpc_helpers.string_field(5)


@dataclass(eq=False, repr=True)
class GetCandlesResponse(_grpc_helpers.Message):
    candles: List["HistoricCandle"] = _grpc_helpers.message_field(1)


@dataclass(eq=True, repr=True, frozen=True)
class HistoricCandle(_grpc_helpers.Message):
    open: Quotation = _grpc_helpers.message_field(1)
    high: Quotation = _grpc_helpers.message_field(2)
    low: Quotation = _grpc_helpers.message_field(3)
    close: Quotation = _grpc_helpers.message_field(4)
    volume: int = _grpc_helpers.int64_field(5)
    time: datetime = _grpc_helpers.message_field(6)
    is_complete: bool = _grpc_helpers.bool_field(7)


@dataclass(eq=False, repr=True)
class GetLastPricesRequest(_grpc_helpers.Message):
    figi: List[str] = _grpc_helpers.string_field(1)
    instrument_id: List[str] = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class GetLastPricesResponse(_grpc_helpers.Message):
    last_prices: List["LastPrice"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class LastPrice(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    price: "Quotation" = _grpc_helpers.message_field(2)
    time: datetime = _grpc_helpers.message_field(3)
    instrument_uid: str = _grpc_helpers.string_field(11)


@dataclass(eq=False, repr=True)
class GetOrderBookRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    depth: int = _grpc_helpers.int32_field(2)
    instrument_id: str = _grpc_helpers.string_field(3)


@dataclass(eq=False, repr=True)
class GetOrderBookResponse(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    depth: int = _grpc_helpers.int32_field(2)
    bids: List["Order"] = _grpc_helpers.message_field(3)
    asks: List["Order"] = _grpc_helpers.message_field(4)
    last_price: "Quotation" = _grpc_helpers.message_field(5)
    close_price: "Quotation" = _grpc_helpers.message_field(6)
    limit_up: "Quotation" = _grpc_helpers.message_field(7)
    limit_down: "Quotation" = _grpc_helpers.message_field(8)
    last_price_ts: datetime = _grpc_helpers.message_field(21)
    close_price_ts: datetime = _grpc_helpers.message_field(22)
    orderbook_ts: datetime = _grpc_helpers.message_field(23)
    instrument_uid: str = _grpc_helpers.string_field(9)


@dataclass(eq=False, repr=True)
class GetTradingStatusRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    instrument_id: str = _grpc_helpers.string_field(2)


@dataclass(eq=False, repr=True)
class GetTradingStatusResponse(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    trading_status: "SecurityTradingStatus" = _grpc_helpers.enum_field(2)
    limit_order_available_flag: bool = _grpc_helpers.bool_field(3)
    market_order_available_flag: bool = _grpc_helpers.bool_field(4)
    api_trade_available_flag: bool = _grpc_helpers.bool_field(5)
    instrument_uid: str = _grpc_helpers.string_field(6)


@dataclass(eq=False, repr=True)
class GetLastTradesRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)
    instrument_id: str = _grpc_helpers.string_field(4)


@dataclass(eq=False, repr=True)
class GetLastTradesResponse(_grpc_helpers.Message):
    trades: List["Trade"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class GetMySubscriptions(_grpc_helpers.Message):
    pass


@dataclass(eq=False, repr=True)
class GetClosePricesRequest(_grpc_helpers.Message):
    instruments: List["InstrumentClosePriceRequest"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class InstrumentClosePriceRequest(_grpc_helpers.Message):
    instrument_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetClosePricesResponse(_grpc_helpers.Message):
    close_prices: List["InstrumentClosePriceResponse"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class InstrumentClosePriceResponse(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    instrument_uid: str = _grpc_helpers.string_field(2)
    price: "Quotation" = _grpc_helpers.message_field(11)
    time: datetime = _grpc_helpers.message_field(21)


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
class OperationTrade(_grpc_helpers.Message):
    trade_id: str = _grpc_helpers.string_field(1)
    date_time: datetime = _grpc_helpers.message_field(2)
    quantity: int = _grpc_helpers.int64_field(3)
    price: "MoneyValue" = _grpc_helpers.message_field(4)


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
    operation_type: "OperationType" = _grpc_helpers.enum_field(13)
    trades: List["OperationTrade"] = _grpc_helpers.message_field(14)
    asset_uid: str = _grpc_helpers.string_field(16)


class CurrencyRequest(_grpc_helpers.Enum):
    RUB = 0
    USD = 1
    EUR = 2


@dataclass(eq=False, repr=True)
class PortfolioRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    currency: CurrencyRequest = _grpc_helpers.enum_field(2)


@dataclass(eq=False, repr=True)
class VirtualPortfolioPosition(_grpc_helpers.Message):
    position_uid: str = _grpc_helpers.string_field(1)
    instrument_uid: str = _grpc_helpers.string_field(2)
    figi: str = _grpc_helpers.string_field(3)
    instrument_type: str = _grpc_helpers.string_field(4)
    quantity: "Quotation" = _grpc_helpers.message_field(5)
    average_position_price: "MoneyValue" = _grpc_helpers.message_field(6)
    expected_yield: "Quotation" = _grpc_helpers.message_field(7)
    expected_yield_fifo: "Quotation" = _grpc_helpers.message_field(8)
    expire_date: datetime = _grpc_helpers.message_field(9)
    current_price: "MoneyValue" = _grpc_helpers.message_field(10)
    average_position_price_fifo: "MoneyValue" = _grpc_helpers.message_field(11)


@dataclass(eq=False, repr=True)
class PortfolioResponse(_grpc_helpers.Message):
    total_amount_shares: "MoneyValue" = _grpc_helpers.message_field(1)
    total_amount_bonds: "MoneyValue" = _grpc_helpers.message_field(2)
    total_amount_etf: "MoneyValue" = _grpc_helpers.message_field(3)
    total_amount_currencies: "MoneyValue" = _grpc_helpers.message_field(4)
    total_amount_futures: "MoneyValue" = _grpc_helpers.message_field(5)
    expected_yield: "Quotation" = _grpc_helpers.message_field(6)
    positions: List["PortfolioPosition"] = _grpc_helpers.message_field(7)
    account_id: str = _grpc_helpers.string_field(8)

    total_amount_options: MoneyValue = _grpc_helpers.message_field(9)
    total_amount_sp: MoneyValue = _grpc_helpers.message_field(10)
    total_amount_portfolio: MoneyValue = _grpc_helpers.message_field(11)
    virtual_positions: List["VirtualPortfolioPosition"] = _grpc_helpers.message_field(
        12
    )


@dataclass(eq=False, repr=True)
class PositionsRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class PositionsResponse(_grpc_helpers.Message):
    money: List["MoneyValue"] = _grpc_helpers.message_field(1)
    blocked: List["MoneyValue"] = _grpc_helpers.message_field(2)
    securities: List["PositionsSecurities"] = _grpc_helpers.message_field(3)
    limits_loading_in_progress: bool = _grpc_helpers.bool_field(4)
    futures: List["PositionsFutures"] = _grpc_helpers.bool_field(5)
    options: List["PositionsOptions"] = _grpc_helpers.bool_field(6)


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
    quantity: "Quotation" = _grpc_helpers.message_field(3)
    average_position_price: "MoneyValue" = _grpc_helpers.message_field(4)
    expected_yield: "Quotation" = _grpc_helpers.message_field(5)
    current_nkd: "MoneyValue" = _grpc_helpers.message_field(6)
    average_position_price_pt: "Quotation" = _grpc_helpers.message_field(7)
    current_price: "MoneyValue" = _grpc_helpers.message_field(8)
    average_position_price_fifo: "MoneyValue" = _grpc_helpers.message_field(9)
    quantity_lots: "Quotation" = _grpc_helpers.message_field(10)
    blocked: bool = _grpc_helpers.bool_field(21)
    position_uid: str = _grpc_helpers.string_field(24)
    instrument_uid: str = _grpc_helpers.string_field(25)
    var_margin: "MoneyValue" = _grpc_helpers.message_field(26)
    expected_yield_fifo: "Quotation" = _grpc_helpers.message_field(27)


@dataclass(eq=False, repr=True)
class PositionsSecurities(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    blocked: int = _grpc_helpers.int64_field(2)
    balance: int = _grpc_helpers.int64_field(3)
    position_uid: str = _grpc_helpers.string_field(4)
    instrument_uid: str = _grpc_helpers.string_field(5)
    exchange_blocked: bool = _grpc_helpers.bool_field(11)
    instrument_type: str = _grpc_helpers.string_field(16)


@dataclass(eq=False, repr=True)
class TradesStreamRequest(_grpc_helpers.Message):
    accounts: List[str] = _grpc_helpers.string_field(1)


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
    account_id: str = _grpc_helpers.string_field(6)
    instrument_uid: str = _grpc_helpers.string_field(7)


@dataclass(eq=False, repr=True)
class OrderTrade(_grpc_helpers.Message):
    date_time: datetime = _grpc_helpers.message_field(1)
    price: "Quotation" = _grpc_helpers.message_field(2)
    quantity: int = _grpc_helpers.int64_field(3)
    trade_id: str = _grpc_helpers.string_field(4)


@dataclass(eq=False, repr=True)
class PostOrderRequest(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    quantity: int = _grpc_helpers.int64_field(2)
    price: "Quotation" = _grpc_helpers.message_field(3)
    direction: "OrderDirection" = _grpc_helpers.enum_field(4)
    account_id: str = _grpc_helpers.string_field(5)
    order_type: "OrderType" = _grpc_helpers.enum_field(6)
    order_id: str = _grpc_helpers.string_field(7)
    instrument_id: str = _grpc_helpers.string_field(8)


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
    instrument_uid: str = _grpc_helpers.string_field(17)


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
    instrument_uid: str = _grpc_helpers.string_field(19)


@dataclass(eq=False, repr=True)
class OrderStage(_grpc_helpers.Message):
    price: "MoneyValue" = _grpc_helpers.message_field(1)
    quantity: int = _grpc_helpers.int64_field(2)
    trade_id: str = _grpc_helpers.string_field(3)


class ReplaceOrderRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    order_id: str = _grpc_helpers.string_field(6)
    idempotency_key: str = _grpc_helpers.string_field(7)
    quantity: int = _grpc_helpers.int64_field(11)
    price: "Quotation" = _grpc_helpers.message_field(12)
    price_type: "PriceType" = _grpc_helpers.enum_field(13)


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
    access_level: "AccessLevel" = _grpc_helpers.message_field(7)

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
    corrected_margin: "MoneyValue" = _grpc_helpers.message_field(6)


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
    tariff: str = _grpc_helpers.string_field(4)


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
    instrument_id: str = _grpc_helpers.string_field(10)


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
    instrument_uid: str = _grpc_helpers.string_field(12)


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


@dataclass(eq=False, repr=True)
class PositionsFutures(_grpc_helpers.Message):
    figi: str = _grpc_helpers.string_field(1)
    blocked: int = _grpc_helpers.int64_field(2)
    balance: int = _grpc_helpers.int64_field(3)
    position_uid: str = _grpc_helpers.string_field(4)
    instrument_uid: str = _grpc_helpers.string_field(5)


@dataclass(eq=False, repr=True)
class PositionsOptions(_grpc_helpers.Message):
    position_uid: str = _grpc_helpers.string_field(1)
    instrument_uid: str = _grpc_helpers.string_field(2)
    blocked: int = _grpc_helpers.int64_field(11)
    balance: int = _grpc_helpers.int64_field(21)


@dataclass(eq=False, repr=True)
class GetDividendsForeignIssuerRequest(_grpc_helpers.Message):
    generate_div_foreign_issuer_report: "GenerateDividendsForeignIssuerReportRequest" = _grpc_helpers.message_field(  # noqa:E501 # pylint:disable=line-too-long
        1, group="payload"
    )
    get_div_foreign_issuer_report: "GetDividendsForeignIssuerReportRequest" = (
        _grpc_helpers.message_field(2, group="payload")
    )


@dataclass(eq=False, repr=True)
class GetDividendsForeignIssuerResponse(_grpc_helpers.Message):
    generate_div_foreign_issuer_report_response: "GenerateDividendsForeignIssuerReportResponse" = _grpc_helpers.message_field(  # noqa:E501 # pylint:disable=line-too-long
        1, group="payload"
    )
    div_foreign_issuer_report: "GetDividendsForeignIssuerReportResponse" = (
        _grpc_helpers.message_field(2, group="payload")
    )


@dataclass(eq=False, repr=True)
class GenerateDividendsForeignIssuerReportRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    from_: datetime = _grpc_helpers.message_field(2)
    to: datetime = _grpc_helpers.message_field(3)


@dataclass(eq=False, repr=True)
class GetDividendsForeignIssuerReportRequest(_grpc_helpers.Message):
    task_id: str = _grpc_helpers.string_field(1)
    page: int = _grpc_helpers.int32_field(2)


@dataclass(eq=False, repr=True)
class GenerateDividendsForeignIssuerReportResponse(_grpc_helpers.Message):
    task_id: str = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class GetDividendsForeignIssuerReportResponse(_grpc_helpers.Message):
    dividends_foreign_issuer_report: List[
        "DividendsForeignIssuerReport"
    ] = _grpc_helpers.message_field(1)
    itemsCount: int = _grpc_helpers.int32_field(2)
    pagesCount: int = _grpc_helpers.int32_field(3)
    page: int = _grpc_helpers.int32_field(4)


@dataclass(eq=False, repr=True)
class DividendsForeignIssuerReport(  # pylint:disable=too-many-instance-attributes
    _grpc_helpers.Message
):
    record_date: datetime = _grpc_helpers.message_field(1)
    payment_date: datetime = _grpc_helpers.message_field(2)
    security_name: str = _grpc_helpers.string_field(3)
    isin: str = _grpc_helpers.string_field(4)
    issuer_country: str = _grpc_helpers.string_field(5)
    quantity: int = _grpc_helpers.int64_field(6)
    dividend: "Quotation" = _grpc_helpers.message_field(7)
    external_commission: "Quotation" = _grpc_helpers.message_field(8)
    dividend_gross: "Quotation" = _grpc_helpers.message_field(9)
    tax: "Quotation" = _grpc_helpers.message_field(10)
    dividend_amount: "Quotation" = _grpc_helpers.message_field(11)
    currency: str = _grpc_helpers.string_field(12)


@dataclass(eq=False, repr=True)
class PortfolioStreamRequest(_grpc_helpers.Message):
    accounts: List[str] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class PortfolioStreamResponse(_grpc_helpers.Message):
    subscriptions: "PortfolioSubscriptionResult" = _grpc_helpers.message_field(
        1, group="payload"
    )
    portfolio: "PortfolioResponse" = _grpc_helpers.message_field(2, group="payload")
    ping: "Ping" = _grpc_helpers.message_field(3, group="payload")


@dataclass(eq=False, repr=True)
class PortfolioSubscriptionResult(_grpc_helpers.Message):
    accounts: List["AccountSubscriptionStatus"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class AccountSubscriptionStatus(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    subscription_status: "PortfolioSubscriptionStatus" = _grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class GetOperationsByCursorRequest(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    instrument_id: str = _grpc_helpers.string_field(2)
    from_: datetime = _grpc_helpers.message_field(6)
    to: datetime = _grpc_helpers.message_field(7)
    cursor: str = _grpc_helpers.string_field(11)
    limit: int = _grpc_helpers.int32_field(12)
    operation_types: List["OperationType"] = _grpc_helpers.message_field(13)
    state: "OperationState" = _grpc_helpers.message_field(14)
    without_commissions: bool = _grpc_helpers.bool_field(15)
    without_trades: bool = _grpc_helpers.bool_field(16)
    without_overnights: bool = _grpc_helpers.bool_field(17)


@dataclass(eq=False, repr=True)
class GetOperationsByCursorResponse(_grpc_helpers.Message):
    has_next: bool = _grpc_helpers.bool_field(1)
    next_cursor: str = _grpc_helpers.string_field(2)
    items: List["OperationItem"] = _grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class OperationItem(_grpc_helpers.Message):
    cursor: str = _grpc_helpers.string_field(1)
    broker_account_id: str = _grpc_helpers.string_field(6)
    id: str = _grpc_helpers.string_field(16)
    parent_operation_id: str = _grpc_helpers.string_field(17)
    name: str = _grpc_helpers.string_field(18)
    date: datetime = _grpc_helpers.message_field(21)
    type: "OperationType" = _grpc_helpers.enum_field(22)
    description: str = _grpc_helpers.string_field(23)
    state: "OperationState" = _grpc_helpers.message_field(24)
    instrument_uid: str = _grpc_helpers.string_field(31)
    figi: str = _grpc_helpers.string_field(32)
    instrument_type: str = _grpc_helpers.string_field(33)
    instrument_kind: "InstrumentType" = _grpc_helpers.enum_field(34)
    payment: "MoneyValue" = _grpc_helpers.message_field(41)
    price: "MoneyValue" = _grpc_helpers.message_field(42)
    commission: "MoneyValue" = _grpc_helpers.message_field(43)
    yield_: "MoneyValue" = _grpc_helpers.message_field(44)
    yield_relative: "Quotation" = _grpc_helpers.message_field(45)
    accrued_int: "MoneyValue" = _grpc_helpers.message_field(46)
    quantity: int = _grpc_helpers.int64_field(51)
    quantity_rest: int = _grpc_helpers.int64_field(52)
    quantity_done: int = _grpc_helpers.int64_field(53)
    cancel_date_time: datetime = _grpc_helpers.message_field(56)
    cancel_reason: str = _grpc_helpers.string_field(57)
    trades_info: "OperationItemTrades" = _grpc_helpers.message_field(61)
    asset_uid: str = _grpc_helpers.string_field(64)


@dataclass(eq=False, repr=True)
class OperationItemTrades(_grpc_helpers.Message):
    trades: List["OperationItemTrade"] = _grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class OperationItemTrade(_grpc_helpers.Message):
    num: str = _grpc_helpers.string_field(1)
    date: datetime = _grpc_helpers.message_field(6)
    quantity: int = _grpc_helpers.int64_field(11)
    price: "MoneyValue" = _grpc_helpers.message_field(16)
    yield_: "MoneyValue" = _grpc_helpers.message_field(21)
    yield_relative: "Quotation" = _grpc_helpers.message_field(22)


@dataclass(eq=False, repr=True)
class PositionsStreamRequest(_grpc_helpers.Message):
    accounts: List[str] = _grpc_helpers.string_field(1)


@dataclass(eq=False, repr=True)
class PositionsStreamResponse(_grpc_helpers.Message):
    subscriptions: "PositionsSubscriptionResult" = _grpc_helpers.message_field(
        1, group="payload"
    )
    position: "PositionData" = _grpc_helpers.message_field(2, group="payload")
    ping: "Ping" = _grpc_helpers.message_field(3, group="payload")


@dataclass(eq=False, repr=True)
class PositionsSubscriptionResult(_grpc_helpers.Message):
    accounts: List["PositionsSubscriptionStatus"] = _grpc_helpers.message_field(1)


@dataclass(eq=False, repr=True)
class PositionsSubscriptionStatus(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    subscription_status: "PositionsAccountSubscriptionStatus" = (
        _grpc_helpers.message_field(6)
    )


@dataclass(eq=False, repr=True)
class PositionData(_grpc_helpers.Message):
    account_id: str = _grpc_helpers.string_field(1)
    money: List["PositionsMoney"] = _grpc_helpers.message_field(2)
    securities: List["PositionsSecurities"] = _grpc_helpers.message_field(3)
    futures: List["PositionsFutures"] = _grpc_helpers.message_field(4)
    options: List["PositionsOptions"] = _grpc_helpers.message_field(5)
    date: datetime = _grpc_helpers.message_field(6)


@dataclass(eq=False, repr=True)
class PositionsMoney(_grpc_helpers.Message):
    available_value: "MoneyValue" = _grpc_helpers.message_field(1)
    blocked_value: "MoneyValue" = _grpc_helpers.message_field(2)
