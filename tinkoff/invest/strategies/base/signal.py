import enum
from dataclasses import dataclass, field


class SignalDirection(enum.Enum):
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass
class Signal:
    pass


@dataclass
class OrderSignal(Signal):
    lots: int
    direction: SignalDirection


@dataclass
class CloseSignal(OrderSignal):
    pass


@dataclass
class OpenSignal(OrderSignal):
    pass


@dataclass
class OpenLongMarketOrder(OpenSignal):
    direction: SignalDirection = field(default=SignalDirection.LONG)


@dataclass
class CloseLongMarketOrder(CloseSignal):
    direction: SignalDirection = field(default=SignalDirection.LONG)


@dataclass
class OpenShortMarketOrder(OpenSignal):
    direction: SignalDirection = field(default=SignalDirection.SHORT)


@dataclass
class CloseShortMarketOrder(CloseSignal):
    direction: SignalDirection = field(default=SignalDirection.SHORT)
