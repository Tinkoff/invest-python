import abc
from typing import Generic, Iterable, TypeVar

TItemId = TypeVar("TItemId")
TItem = TypeVar("TItem")


class IItemStorage(Generic[TItemId, TItem], abc.ABC):
    @abc.abstractmethod
    def get_all(self) -> Iterable[TItem]:
        ...

    @abc.abstractmethod
    def update(self, item_id: TItemId, new_item: TItem) -> None:
        ...

    @abc.abstractmethod
    def add(self, item: TItem) -> None:
        ...

    @abc.abstractmethod
    def delete(self, item: TItemId) -> None:
        ...
