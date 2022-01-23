from abc import ABC

from tinkoff.invest import OrderState
from tinkoff.invest.storage.item_storage import IItemStorage


class IOrderStorage(IItemStorage[str, OrderState], ABC):
    ...
