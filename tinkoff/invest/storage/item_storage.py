import abc
from typing import Generic, Iterable, TypeVar, Tuple

TItemId = TypeVar("TItemId")
TItem = TypeVar("TItem")


class IItemStorage(Generic[TItemId, TItem], abc.ABC):
    @abc.abstractmethod
    def items(self) -> Iterable[Tuple[TItemId, TItem]]:
        ...

    @abc.abstractmethod
    def get(self, item_id: TItemId) -> TItem:
        ...

    @abc.abstractmethod
    def set(self, item_id: TItemId, new_item: TItem) -> None:
        ...

    @abc.abstractmethod
    def delete(self, item_id: TItemId) -> None:
        ...
