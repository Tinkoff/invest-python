class StrategyError(Exception):
    pass


class NotEnoughData(StrategyError):
    pass


class MarginalTradeIsNotActive(StrategyError):
    pass


class CandleEventForDateNotFound(StrategyError):
    pass


class UnknownSignal(StrategyError):
    pass
