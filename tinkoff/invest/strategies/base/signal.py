from dataclasses import dataclass


@dataclass
class Signal:
    pass


@dataclass
class OrderSignal(Signal):
    lots: int


@dataclass
class OpenLongMarketOrder(OrderSignal):
    pass


@dataclass
class CloseLongMarketOrder(OrderSignal):
    pass


@dataclass
class OpenShortMarketOrder(OrderSignal):
    pass


@dataclass
class CloseShortMarketOrder(OrderSignal):
    pass
