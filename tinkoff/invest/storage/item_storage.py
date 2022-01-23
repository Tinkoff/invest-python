import abc
from typing import Iterable, TypeVar, Generic


TId = TypeVar("TId")
TItem = TypeVar("TItem")


class IItemStorage(Generic[TId, TItem], abc.ABC):
    @abc.abstractmethod
    def get_all(self) -> Iterable[TItem]: ...

    @abc.abstractmethod
    def add(self, item: TItem) -> None: ...

    @abc.abstractmethod
    def delete(self, item: TId) -> None: ...
