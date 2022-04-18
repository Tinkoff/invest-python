from typing import Protocol


class ITrader(Protocol):
    def trade(self):
        pass
