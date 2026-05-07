from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Generic, TypeVar


T = TypeVar("T")
U = TypeVar("U")


class BookCollection(Generic[T]):
    """коллекция с функциональными операциями и поддержкой chain api"""

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._items: list[T] = list(items) if items is not None else []

    def add(self, item: T) -> None:
        self._items.append(item)

    def to_list(self) -> list[T]:
        return list(self._items)

    def sort_by(
        self,
        key_func: Callable[[T], object],
        reverse: bool = False,
    ) -> BookCollection[T]:
        return BookCollection(sorted(self._items, key=key_func, reverse=reverse))

    def filter_by(self, predicate: Callable[[T], bool]) -> BookCollection[T]:
        return BookCollection(filter(predicate, self._items))

    def apply(self, func: Callable[[T], U]) -> BookCollection[U]:
        return BookCollection(map(func, self._items))

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> T:
        return self._items[index]

