class StrategyError(Exception):
    pass


class NotEnoughData(StrategyError):
    pass


class MarginalTradeIsNotActive(StrategyError):
    pass


class InsufficientMarginalTradeFunds(StrategyError):
    pass


class CandleEventForDateNotFound(StrategyError):
    pass


class UnknownSignal(StrategyError):
    pass


class OldCandleObservingError(StrategyError):
    pass


class MarketDataNotAvailableError(StrategyError):
    pass


class StrategySupervisorError(Exception):
    pass


class EventsWereNotSupervised(StrategySupervisorError):
    pass
