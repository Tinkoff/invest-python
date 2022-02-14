from dataclasses import dataclass


@dataclass
class Signal:
    pass


@dataclass
class OrderSignal(Signal):
    lots: int


@dataclass
class CloseSignal(OrderSignal):
    pass


@dataclass
class OpenSignal(OrderSignal):
    pass


@dataclass
class OpenLongMarketOrder(OpenSignal):
    pass


@dataclass
class CloseLongMarketOrder(CloseSignal):
    pass


@dataclass
class OpenShortMarketOrder(OpenSignal):
    pass


@dataclass
class CloseShortMarketOrder(CloseSignal):
    pass
