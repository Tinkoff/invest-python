from abc import ABC

from tinkoff.invest import PortfolioPosition
from tinkoff.invest.storage.item_storage import IItemStorage


class IPositionsStorage(IItemStorage[str, PortfolioPosition], ABC):
    ...
