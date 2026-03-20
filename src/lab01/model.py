from __future__ import annotations

try:
    from .validate import (
        validate_author,
        validate_inventory_id,
        validate_pages,
        validate_price,
        validate_state,
        validate_title,
        validate_year,
    )
except ImportError:
    from validate import (
        validate_author,
        validate_inventory_id,
        validate_pages,
        validate_price,
        validate_state,
        validate_title,
        validate_year,
    )


class BookValidationError(ValueError):
    """Исключение для ошибок валидации данных книги"""


class BookState:
    AVAILABLE: str = "available"
    CHECKED_OUT: str = "checked_out"
    LOST: str = "lost"


class Book:
    """Модель книги в библиотеке с логическими состояниями и валидацией"""

    ALLOWED_STATES: tuple[str, ...] = (
        BookState.AVAILABLE,
        BookState.CHECKED_OUT,
        BookState.LOST,
    )

    MIN_YEAR: int = 1450
    MAX_YEAR: int = 2026
    MIN_PRICE: float = 0.0
    MIN_PAGES: int = 1

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        pages: int,
        price: float,
        inventory_id: str,
        state: str = BookState.AVAILABLE,
    ) -> None:
        self._title: str = validate_title(title, BookValidationError)
        self._author: str = validate_author(author, BookValidationError)
        self._year: int = validate_year(
            year,
            self.MIN_YEAR,
            self.MAX_YEAR,
            BookValidationError,
        )
        self._pages: int = validate_pages(pages, self.MIN_PAGES, BookValidationError)
        self._price: float = validate_price(price, self.MIN_PRICE, BookValidationError)
        self._inventory_id: str = validate_inventory_id(inventory_id, BookValidationError)
        self._state: str = validate_state(state, self.ALLOWED_STATES, BookValidationError)

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def year(self) -> int:
        return self._year

    @property
    def pages(self) -> int:
        return self._pages

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        self._price = validate_price(value, self.MIN_PRICE, BookValidationError)

    @property
    def inventory_id(self) -> str:
        return self._inventory_id

    @property
    def state(self) -> str:
        return self._state

    def __str__(self) -> str:
        return (
            f"Book '{self._title}' by {self._author} "
            f"({self._year}, {self._pages} pages, {self._price:.2f}₽) "
            f"[{self._inventory_id}] state={self._state}"
        )

    def __repr__(self) -> str:
        return (
            "Book("
            f"title={self._title!r}, "
            f"author={self._author!r}, "
            f"year={self._year!r}, "
            f"pages={self._pages!r}, "
            f"price={self._price!r}, "
            f"inventory_id={self._inventory_id!r}, "
            f"state={self._state!r}"
            ")"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self._inventory_id == other._inventory_id

    
    def checkout(self) -> None:
        """Выдать книгу читателю"""
        if self._state != BookState.AVAILABLE:
            raise BookValidationError(
                f"Нельзя выдать книгу в состоянии {self._state!r}"
                f"Допустимо только из состояния {BookState.AVAILABLE!r}."
            )
        self._state = BookState.CHECKED_OUT

    def return_book(self) -> None:
        """Вернуть книгу в фонд библиотеки"""
        if self._state != BookState.CHECKED_OUT:
            raise BookValidationError(
                f"Нельзя вернуть книгу в состоянии {self._state!r}"
                f"Допустимо только из состояния {BookState.CHECKED_OUT!r}"
            )
        self._state = BookState.AVAILABLE

    def mark_lost(self) -> None:
        """Отметить книгу как утерянную"""
        if self._state not in (BookState.AVAILABLE, BookState.CHECKED_OUT):
            raise BookValidationError(
                f"Нельзя пометить книгу как утерянную из состояния {self._state!r}."
            )
        self._state = BookState.LOST
