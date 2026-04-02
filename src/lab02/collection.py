"""Контейнер `Library` для хранения объектов `Book` (ЛР-2)."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator

try:
    from .model import Book, BookState
except ImportError:
    from model import Book, BookState


class LibraryError(Exception):
    """Базовое исключение операций библиотечной коллекции."""


class LibraryTypeError(LibraryError, TypeError):
    """Попытка добавить или удалить объект недопустимого типа."""


class DuplicateBookError(LibraryError):
    """Книга с таким инвентарным номером уже есть в коллекции."""


class BookNotFoundError(LibraryError):
    """Указанная книга отсутствует в коллекции."""


class Library:
    """Коллекция книг библиотеки: хранение, поиск, сортировка, фильтрация."""

    def __init__(self) -> None:
        self._items: list[Book] = []

    def add(self, item: Book) -> None:
        if not isinstance(item, Book):
            raise LibraryTypeError(
                f"В коллекцию можно добавлять только объекты Book, получено: {type(item).__name__!r}."
            )
        if any(existing.inventory_id == item.inventory_id for existing in self._items):
            raise DuplicateBookError(
                f"Книга с инвентарным номером {item.inventory_id!r} уже есть в коллекции."
            )
        self._items.append(item)

    def remove(self, item: Book) -> None:
        if not isinstance(item, Book):
            raise LibraryTypeError(
                f"Удалять можно только объекты Book, получено: {type(item).__name__!r}."
            )
        try:
            self._items.remove(item)
        except ValueError as exc:
            raise BookNotFoundError("Указанная книга отсутствует в коллекции.") from exc

    def get_all(self) -> list[Book]:
        return list(self._items)

    def find_by_title(self, title: str) -> list[Book]:
        return [book for book in self._items if book.title == title]

    def find_by_inventory_id(self, inventory_id: str) -> Book | None:
        for book in self._items:
            if book.inventory_id == inventory_id:
                return book
        return None

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Book]:
        return iter(self._items)

    def __getitem__(self, index: int) -> Book:
        return self._items[index]

    def remove_at(self, index: int) -> Book:
        return self._items.pop(index)

    def sort(self, key: Callable[[Book], object], reverse: bool = False) -> None:
        self._items.sort(key=key, reverse=reverse)

    def sort_by_title(self, reverse: bool = False) -> None:
        self.sort(key=lambda b: b.title, reverse=reverse)

    def sort_by_price(self, reverse: bool = False) -> None:
        self.sort(key=lambda b: b.price, reverse=reverse)

    def sort_by_year(self, reverse: bool = False) -> None:
        self.sort(key=lambda b: b.year, reverse=reverse)

    def _new_with(self, books: Iterable[Book]) -> Library:
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


__all__ = (
    "BookNotFoundError",
    "DuplicateBookError",
    "Library",
    "LibraryError",
    "LibraryTypeError",
)
