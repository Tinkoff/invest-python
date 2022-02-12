import abc


class ITrader(abc.ABC):
    @abc.abstractmethod
    def trade(self):
        pass
