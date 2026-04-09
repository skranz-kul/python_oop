from __future__ import annotations

try:
    from ..lib.book_validators import (
        validate_float_min,
        validate_int_min,
        validate_non_empty_string,
        validate_state,
        validate_year,
    )
except ImportError:
    from lib.book_validators import (  # type: ignore[no-redef]
        validate_float_min,
        validate_int_min,
        validate_non_empty_string,
        validate_state,
        validate_year,
    )


class BookValidationError(ValueError):
    """Исключение для ошибок валидации модели книги."""


class BookState:
    AVAILABLE: str = "available"
    CHECKED_OUT: str = "checked_out"
    LOST: str = "lost"


class Book:
    """Базовый класс книги для иерархии ЛР-3."""

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
        self._title: str = validate_non_empty_string(
            title,
            "Название книги",
            BookValidationError,
        )
        self._author: str = validate_non_empty_string(
            author,
            "Автор",
            BookValidationError,
        )
        self._year: int = validate_year(
            year,
            self.MIN_YEAR,
            self.MAX_YEAR,
            BookValidationError,
        )
        self._pages: int = validate_int_min(
            pages,
            self.MIN_PAGES,
            "Количество страниц",
            BookValidationError,
        )
        self._price: float = validate_float_min(
            price,
            self.MIN_PRICE,
            "Цена",
            BookValidationError,
        )
        self._inventory_id: str = validate_non_empty_string(
            inventory_id,
            "Инвентарный номер",
            BookValidationError,
        )
        self._state: str = validate_state(
            state,
            self.ALLOWED_STATES,
            BookValidationError,
        )

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
        self._price = validate_float_min(
            value,
            self.MIN_PRICE,
            "Цена",
            BookValidationError,
        )

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
            f"title={self._title!r}, author={self._author!r}, year={self._year!r}, "
            f"pages={self._pages!r}, price={self._price!r}, "
            f"inventory_id={self._inventory_id!r}, state={self._state!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self._inventory_id == other._inventory_id

    def checkout(self) -> None:
        if self._state != BookState.AVAILABLE:
            raise BookValidationError(
                f"Нельзя выдать книгу в состоянии {self._state!r}. "
                f"Допустимо только {BookState.AVAILABLE!r}."
            )
        self._state = BookState.CHECKED_OUT

    def return_book(self) -> None:
        if self._state != BookState.CHECKED_OUT:
            raise BookValidationError(
                f"Нельзя вернуть книгу в состоянии {self._state!r}. "
                f"Допустимо только {BookState.CHECKED_OUT!r}."
            )
        self._state = BookState.AVAILABLE

    def mark_lost(self) -> None:
        if self._state not in (BookState.AVAILABLE, BookState.CHECKED_OUT):
            raise BookValidationError(
                f"Нельзя пометить книгу как утерянную из состояния {self._state!r}."
            )
        self._state = BookState.LOST

    def calculate_access_fee(self) -> float:
        """Общий интерфейс поведения для полиморфизма."""
        return round(self._price, 2)

