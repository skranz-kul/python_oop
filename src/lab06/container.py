"""ЛР-6: Generic-контейнер `TypedCollection` и протоколы структурной типизации."""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable, Iterator
from typing import Generic, Protocol, TypeVar

try:
    from src.lab02.collection import (
        BookNotFoundError,
        DuplicateBookError,
        LibraryError,
        LibraryTypeError,
    )
    from src.lab02.model import Book as Lab02Book
    from src.lab02.model import BookState
except ImportError:  # pragma: no cover - запуск не из корня проекта
    try:
        from lab02.collection import (
            BookNotFoundError,
            DuplicateBookError,
            LibraryError,
            LibraryTypeError,
        )
        from lab02.model import Book as Lab02Book
        from lab02.model import BookState
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "lab06.container требует пакеты lab02 (исключения и BookState)."
        ) from exc

try:
    from src.lab03.base import Book as Lab03Book
    from src.lab03.models import AudioBook, Ebook, PrintedBook
except ImportError:  # pragma: no cover
    try:
        from lab03.base import Book as Lab03Book  # type: ignore[no-redef]
        from lab03.models import AudioBook, Ebook, PrintedBook  # type: ignore[no-redef]
    except ImportError:
        Lab03Book = None  # type: ignore[assignment,misc]
        AudioBook = None  # type: ignore[assignment,misc]
        Ebook = None  # type: ignore[assignment,misc]
        PrintedBook = None  # type: ignore[assignment,misc]

try:
    from src.lab04.interfaces import Comparable, Printable
except ImportError:  # pragma: no cover
    try:
        from lab04.interfaces import Comparable, Printable  # type: ignore[no-redef]
    except ImportError:
        Comparable = None  # type: ignore[assignment,misc]
        Printable = None  # type: ignore[assignment,misc]

logger = logging.getLogger(__name__)

__all__ = (
    "BookNotFoundError",
    "Comparable",
    "D",
    "Displayable",
    "DuplicateBookError",
    "LibraryError",
    "LibraryItem",
    "LibraryTypeError",
    "Printable",
    "R",
    "S",
    "Scorable",
    "T",
    "TypedCollection",
)


class LibraryItem(Protocol):
    """Минимальный контракт сущности «книга в фонде» для API, унаследованного от `Library`."""

    @property
    def title(self) -> str: ...

    @property
    def inventory_id(self) -> str: ...

    @property
    def state(self) -> str: ...

    @property
    def price(self) -> float: ...

    @property
    def year(self) -> int: ...


class Displayable(Protocol):
    def display(self) -> str: ...


class Scorable(Protocol):
    def score(self) -> float: ...


T = TypeVar("T")
R = TypeVar("R")
D = TypeVar("D", bound=Displayable)
S = TypeVar("S", bound=Scorable)


class TypedCollection(Generic[T]):
    """Типизированная коллекция с интерфейсом `Library` и обобщёнными `find`/`filter`/`map`."""

    def __init__(
        self,
        *,
        allowed_item_type: type | tuple[type, ...] | None = None,
    ) -> None:
        self._items: list[T] = []
        self._allowed_item_type: type | tuple[type, ...] | None = allowed_item_type

    @staticmethod
    def default_library_book_types() -> tuple[type[object], ...]:
        """Типы экземпляров книг, совместимые с `Library` (ЛР-2) и иерархией ЛР-3."""
        if Lab03Book is None:
            return (Lab02Book,)
        return (Lab02Book, Lab03Book)

    def _ensure_instance_allowed(self, item: object, *, operation: str) -> None:
        if self._allowed_item_type is None:
            return
        if not isinstance(item, self._allowed_item_type):
            logger.warning(
                "Отклонён тип при %s: %s",
                operation,
                type(item).__name__,
            )
            raise LibraryTypeError(
                f"Операция {operation}: недопустимый тип {type(item).__name__}."
            )

    def _inventory_id_of(self, item: object) -> str | None:
        inv = getattr(item, "inventory_id", None)
        return inv if isinstance(inv, str) else None

    def add(self, item: T) -> None:
        self._ensure_instance_allowed(item, operation="add")
        inventory_id = self._inventory_id_of(item)
        if inventory_id is not None:
            if any(self._inventory_id_of(stored) == inventory_id for stored in self._items):
                raise DuplicateBookError(
                    f"Книга с номером {inventory_id} уже есть в коллекции"
                )
        self._items.append(item)

    def remove(self, item: T) -> None:
        self._ensure_instance_allowed(item, operation="remove")
        try:
            self._items.remove(item)
        except ValueError as exc:
            raise BookNotFoundError("Указанная книга отсутствует в коллекции") from exc

    def get_all(self) -> list[T]:
        return list(self._items)

    def find_by_title(self: TypedCollection[LibraryItem], title: str) -> list[LibraryItem]:
        return [book for book in self._items if book.title == title]

    def find_by_inventory_id(
        self: TypedCollection[LibraryItem],
        inventory_id: str,
    ) -> LibraryItem | None:
        for book in self._items:
            if book.inventory_id == inventory_id:
                return book
        return None

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __getitem__(self, index: int) -> T:
        return self._items[index]

    def remove_at(self, index: int) -> T:
        return self._items.pop(index)

    def sort(self, key: Callable[[T], object], reverse: bool = False) -> None:
        self._items.sort(key=key, reverse=reverse)

    def sort_by_title(self: TypedCollection[LibraryItem], reverse: bool = False) -> None:
        self.sort(key=lambda book: book.title, reverse=reverse)

    def sort_by_price(self: TypedCollection[LibraryItem], reverse: bool = False) -> None:
        self.sort(key=lambda book: book.price, reverse=reverse)

    def sort_by_year(self: TypedCollection[LibraryItem], reverse: bool = False) -> None:
        self.sort(key=lambda book: book.year, reverse=reverse)

    def _new_with(self, books: Iterable[T]) -> TypedCollection[T]:
        new_collection = TypedCollection(allowed_item_type=self._allowed_item_type)
        for book in books:
            new_collection.add(book)
        return new_collection

    def get_available(self: TypedCollection[LibraryItem]) -> TypedCollection[LibraryItem]:
        return self._new_with(b for b in self._items if b.state == BookState.AVAILABLE)

    def get_checked_out(self: TypedCollection[LibraryItem]) -> TypedCollection[LibraryItem]:
        return self._new_with(b for b in self._items if b.state == BookState.CHECKED_OUT)

    def get_expensive(
        self: TypedCollection[LibraryItem],
        min_price: float,
    ) -> TypedCollection[LibraryItem]:
        return self._new_with(b for b in self._items if b.price >= min_price)

    def get_only_printed(self: TypedCollection[LibraryItem]) -> TypedCollection[LibraryItem]:
        if PrintedBook is None:
            return TypedCollection(allowed_item_type=self._allowed_item_type)
        return self._new_with(b for b in self._items if isinstance(b, PrintedBook))

    def get_only_ebooks(self: TypedCollection[LibraryItem]) -> TypedCollection[LibraryItem]:
        if Ebook is None:
            return TypedCollection(allowed_item_type=self._allowed_item_type)
        return self._new_with(b for b in self._items if isinstance(b, Ebook))

    def get_only_audio_books(self: TypedCollection[LibraryItem]) -> TypedCollection[LibraryItem]:
        if AudioBook is None:
            return TypedCollection(allowed_item_type=self._allowed_item_type)
        return self._new_with(b for b in self._items if isinstance(b, AudioBook))

    def get_printable(self) -> list[object]:
        if Printable is None:
            return []
        return [item for item in self._items if isinstance(item, Printable)]

    def get_comparable(self) -> list[object]:
        if Comparable is None:
            return []
        return [item for item in self._items if isinstance(item, Comparable)]

    def find(self, predicate: Callable[[T], bool]) -> T | None:
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> list[R]:
        return [transform(item) for item in self._items]
