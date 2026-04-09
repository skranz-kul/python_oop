"""Контейнер `Library` для хранения книг (ЛР-2/ЛР-3)."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import TYPE_CHECKING

try:
    from .model import Book as Lab02Book
    from .model import BookState
except ImportError:
    from model import Book as Lab02Book, BookState

try:
    from ..lab03.base import Book as Lab03Book
    from ..lab03.models import AudioBook, Ebook, PrintedBook
except ImportError:
    try:
        from lab03.base import Book as Lab03Book  # type: ignore[no-redef]
        from lab03.models import AudioBook, Ebook, PrintedBook  # type: ignore[no-redef]
    except ImportError:
        Lab03Book = None
        AudioBook = None
        Ebook = None
        PrintedBook = None

if TYPE_CHECKING:
    from ..lab03.base import Book as Lab03BookType

    SupportedBook = Lab02Book | Lab03BookType
else:
    SupportedBook = Lab02Book


class LibraryError(Exception):
    """Базовое исключение операций библиотечной коллекции."""


class LibraryTypeError(LibraryError, TypeError):
    """Попытка добавить или удалить объект недопустимого типа."""


class DuplicateBookError(LibraryError):
    """Книга с таким инвентарным номером уже есть в коллекции."""


class BookNotFoundError(LibraryError):
    """указанная книга отсутствует в коллекции"""


class Library:
    """Коллекция книг библиотеки: хранение, поиск, сортировка, фильтрация"""

    def __init__(self) -> None:
        self._items: list[SupportedBook] = []

    @staticmethod
    def _allowed_types() -> tuple[type[object], ...]:
        if Lab03Book is None:
            return (Lab02Book,)
        return (Lab02Book, Lab03Book)

    def add(self, item: SupportedBook) -> None:
        if not isinstance(item, self._allowed_types()):
            raise LibraryTypeError(
                f"В коллекцию можно добавлять только объекты Book, получено: "
                f"{type(item).__name__}."
            )
        if any(stored.inventory_id == item.inventory_id for stored in self._items):
            raise DuplicateBookError(
                f"Книга с номером {item.inventory_id} уже есть в коллекции"
            )
        self._items.append(item)

    def remove(self, item: SupportedBook) -> None:
        if not isinstance(item, self._allowed_types()):
            raise LibraryTypeError(
                f"Удалять можно только объекты Book, получено: {type(item).__name__}."
            )
        try:
            self._items.remove(item)
        except ValueError as exc:
            raise BookNotFoundError("Указанная книга отсутствует в коллекции") from exc

    def get_all(self) -> list[SupportedBook]:
        return list(self._items)

    def find_by_title(self, title: str) -> list[SupportedBook]:
        return [book for book in self._items if book.title == title]

    def find_by_inventory_id(self, inventory_id: str) -> SupportedBook | None:
        for book in self._items:
            if book.inventory_id == inventory_id:
                return book
        return None

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[SupportedBook]:
        return iter(self._items)

    def __getitem__(self, index: int) -> SupportedBook:
        return self._items[index]

    def remove_at(self, index: int) -> SupportedBook:
        return self._items.pop(index)

    def sort(
        self,
        key: Callable[[SupportedBook], object],
        reverse: bool = False,
    ) -> None:
        self._items.sort(key=key, reverse=reverse)

    def sort_by_title(self, reverse: bool = False) -> None:
        self.sort(key=lambda book: book.title, reverse=reverse)

    def sort_by_price(self, reverse: bool = False) -> None:
        self.sort(key=lambda book: book.price, reverse=reverse)

    def sort_by_year(self, reverse: bool = False) -> None:
        self.sort(key=lambda book: book.year, reverse=reverse)

    def _new_with(self, books: Iterable[SupportedBook]) -> Library:
        library = Library()
        for book in books:
            library.add(book)
        return library

    def get_available(self) -> Library:
        return self._new_with(b for b in self._items if b.state == BookState.AVAILABLE)

    def get_checked_out(self) -> Library:
        return self._new_with(b for b in self._items if b.state == BookState.CHECKED_OUT)

    def get_expensive(self, min_price: float) -> Library:
        return self._new_with(b for b in self._items if b.price >= min_price)

    # ЛР-3: фильтрация по типам наследников
    def get_only_printed(self) -> Library:
        if PrintedBook is None:
            return Library()
        return self._new_with(b for b in self._items if isinstance(b, PrintedBook))

    def get_only_ebooks(self) -> Library:
        if Ebook is None:
            return Library()
        return self._new_with(b for b in self._items if isinstance(b, Ebook))

    def get_only_audio_books(self) -> Library:
        if AudioBook is None:
            return Library()
        return self._new_with(b for b in self._items if isinstance(b, AudioBook))


__all__ = (
    "BookNotFoundError",
    "DuplicateBookError",
    "Library",
    "LibraryError",
    "LibraryTypeError",
)
