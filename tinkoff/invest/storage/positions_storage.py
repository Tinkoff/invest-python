from abc import ABC
from typing import Iterable, Tuple

from tinkoff.invest import PortfolioPosition
from tinkoff.invest.storage.item_storage import IItemStorage


class IPositionsStorage(IItemStorage[str, PortfolioPosition], ABC):
    pass


class PositionsStorage(IPositionsStorage):
    def items(self) -> Iterable[Tuple[str, PortfolioPosition]]:
        pass

    def get(self, item_id: str) -> PortfolioPosition:
        pass

    def set(self, item_id: str, new_item: PortfolioPosition) -> None:
        pass

    def delete(self, item_id: str) -> None:
        pass
