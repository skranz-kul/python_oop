from __future__ import annotations


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
        self._title: str = self._validate_title(title)
        self._author: str = self._validate_author(author)
        self._year: int = self._validate_year(year)
        self._pages: int = self._validate_pages(pages)
        self._price: float = self._validate_price(price)
        self._inventory_id: str = self._validate_inventory_id(inventory_id)
        self._state: str = self._validate_state(state)

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
        self._price = self._validate_price(value)

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

    
    def _validate_title(self, value: str) -> str:
        if not isinstance(value, str):
            raise BookValidationError("Название книги должно быть строкой.")
        cleaned = value.strip()
        if not cleaned:
            raise BookValidationError("Название книги не может быть пустым.")
        return cleaned

    def _validate_author(self, value: str) -> str:
        if not isinstance(value, str):
            raise BookValidationError("Автор должен быть строкой.")
        cleaned = value.strip()
        if not cleaned:
            raise BookValidationError("Имя автора не может быть пустым.")
        return cleaned

    def _validate_year(self, value: int) -> int:
        if not isinstance(value, int):
            raise BookValidationError("Год издания должен быть целым числом.")
        if not (self.MIN_YEAR <= value <= self.MAX_YEAR):
            raise BookValidationError(
                f"Год издания должен быть в диапазоне "
                f"[{self.MIN_YEAR}, {self.MAX_YEAR}]."
            )
        return value

    def _validate_pages(self, value: int) -> int:
        if not isinstance(value, int):
            raise BookValidationError("Количество страниц должно быть целым числом.")
        if value < self.MIN_PAGES:
            raise BookValidationError(
                f"Количество страниц должно быть не меньше {self.MIN_PAGES}."
            )
        return value

    def _validate_price(self, value: float) -> float:
        if not isinstance(value, (int, float)):
            raise BookValidationError("Цена должна быть числом.")
        price = float(value)
        if price < self.MIN_PRICE:
            raise BookValidationError(
                f"Цена не может быть меньше {self.MIN_PRICE:.2f}."
            )
        return round(price, 2)

    def _validate_state(self, value: str) -> str:
        if not isinstance(value, str):
            raise BookValidationError("Состояние должно быть строкой.")
        if value not in self.ALLOWED_STATES:
            allowed = ", ".join(self.ALLOWED_STATES)
            raise BookValidationError(
                f"Недопустимое состояние {value!r}. "
                f"Разрешённые значения: {allowed}."
            )
        return value

    def _validate_inventory_id(self, value: str) -> str:
        if not isinstance(value, str):
            raise BookValidationError("Инвентарный номер должен быть строкой.")
        cleaned = value.strip()
        if not cleaned:
            raise BookValidationError("Инвентарный номер не может быть пустым.")
        return cleaned


