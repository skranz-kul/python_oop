from __future__ import annotations

from typing import Callable


ErrorFactory = Callable[[str], Exception]


def validate_title(value: str, error_factory: ErrorFactory) -> str:
    if not isinstance(value, str):
        raise error_factory("Название книги должно быть строкой.")
    cleaned = value.strip()
    if not cleaned:
        raise error_factory("Название книги не может быть пустым.")
    return cleaned


def validate_author(value: str, error_factory: ErrorFactory) -> str:
    if not isinstance(value, str):
        raise error_factory("Автор должен быть строкой.")
    cleaned = value.strip()
    if not cleaned:
        raise error_factory("Имя автора не может быть пустым.")
    return cleaned


def validate_year(
    value: int,
    min_year: int,
    max_year: int,
    error_factory: ErrorFactory,
) -> int:
    if not isinstance(value, int):
        raise error_factory("Год издания должен быть целым числом.")
    if not (min_year <= value <= max_year):
        raise error_factory(
            f"Год издания должен быть в диапазоне [{min_year}, {max_year}]."
        )
    return value


def validate_pages(value: int, min_pages: int, error_factory: ErrorFactory) -> int:
    if not isinstance(value, int):
        raise error_factory("Количество страниц должно быть целым числом.")
    if value < min_pages:
        raise error_factory(f"Количество страниц должно быть не меньше {min_pages}.")
    return value


def validate_price(value: float, min_price: float, error_factory: ErrorFactory) -> float:
    if not isinstance(value, (int, float)):
        raise error_factory("Цена должна быть числом.")
    price = float(value)
    if price < min_price:
        raise error_factory(f"Цена не может быть меньше {min_price:.2f}.")
    return round(price, 2)


def validate_state(
    value: str,
    allowed_states: tuple[str, ...],
    error_factory: ErrorFactory,
) -> str:
    if not isinstance(value, str):
        raise error_factory("Состояние должно быть строкой.")
    if value not in allowed_states:
        allowed = ", ".join(allowed_states)
        raise error_factory(
            f"Недопустимое состояние {value!r}. Разрешённые значения: {allowed}."
        )
    return value


def validate_inventory_id(value: str, error_factory: ErrorFactory) -> str:
    if not isinstance(value, str):
        raise error_factory("Инвентарный номер должен быть строкой.")
    cleaned = value.strip()
    if not cleaned:
        raise error_factory("Инвентарный номер не может быть пустым.")
    return cleaned
