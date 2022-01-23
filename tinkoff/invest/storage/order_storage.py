from abc import ABC

from tinkoff.invest.schemas import OrderState
from tinkoff.invest.storage.item_storage import IItemStorage


class IOrdersStorage(IItemStorage[str, OrderState], ABC):
    ...
