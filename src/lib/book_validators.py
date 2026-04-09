from __future__ import annotations

from typing import Callable


ErrorFactory = Callable[[str], Exception]


def validate_non_empty_string(
    value: str,
    field_name: str,
    error_factory: ErrorFactory,
) -> str:
    if not isinstance(value, str):
        raise error_factory(f"{field_name} должно быть строкой.")
    cleaned = value.strip()
    if not cleaned:
        raise error_factory(f"{field_name} не может быть пустым.")
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


def validate_int_min(
    value: int,
    min_value: int,
    field_name: str,
    error_factory: ErrorFactory,
) -> int:
    if not isinstance(value, int):
        raise error_factory(f"{field_name} должно быть целым числом.")
    if value < min_value:
        raise error_factory(f"{field_name} должно быть не меньше {min_value}.")
    return value


def validate_float_min(
    value: float,
    min_value: float,
    field_name: str,
    error_factory: ErrorFactory,
) -> float:
    if not isinstance(value, (int, float)):
        raise error_factory(f"{field_name} должно быть числом.")
    converted = float(value)
    if converted < min_value:
        raise error_factory(f"{field_name} не может быть меньше {min_value:.2f}.")
    return round(converted, 2)


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

