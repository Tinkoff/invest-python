from typing import Iterable

from tinkoff.invest import PortfolioPosition
from tinkoff.invest.storage.positions_storage import IPositionsStorage


class PositionsStorage(IPositionsStorage):
    def get_all(self) -> Iterable[PortfolioPosition]:
        pass

    def add(self, item: PortfolioPosition) -> None:
        pass

    def delete(self, item: str) -> None:
        pass
