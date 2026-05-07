from __future__ import annotations

from copy import deepcopy
from typing import Callable

from src.lab04.models import AudioBook, Book, Ebook, PrintedBook


BookItem = Book | PrintedBook | Ebook | AudioBook


def by_title(item: BookItem) -> str:
    """возвращает ключ сортировки по названию"""
    return item.title


def by_price(item: BookItem) -> float:
    """возвращает ключ сортировки по цене"""
    return item.price


def by_multi(item: BookItem) -> tuple[object, ...]:
    """возвращает составной ключ сортировки по названию, году и цене"""
    return (item.title, item.year, item.price)


def is_expensive(item: BookItem, min_price: float = 1200.0) -> bool:
    """проверяет что цена книги не ниже порога"""
    return item.price >= min_price


def is_ebook(item: BookItem) -> bool:
    """проверяет что объект является ebook"""
    return isinstance(item, Ebook)


def to_title(item: BookItem) -> str:
    """преобразует объект книги в название"""
    return item.title


def to_summary(item: BookItem) -> str:
    """преобразует объект книги в краткую строку"""
    return f"{item.__class__.__name__}: {item.title} ({item.price:.2f}₽)"


def make_max_price_filter(max_price: float) -> Callable[[BookItem], bool]:
    """создает предикат фильтрации книг по максимальной цене"""

    def predicate(item: BookItem) -> bool:
        return item.price <= max_price

    return predicate


class DiscountStrategy:
    """callable-стратегия применения скидки к цене книги"""

    def __init__(self, discount_rate: float) -> None:
        if not (0.0 <= discount_rate < 1.0):
            raise ValueError("discount_rate должен быть в диапазоне [0.0, 1.0)")
        self._discount_rate = discount_rate

    def __call__(self, item: BookItem) -> BookItem:
        discounted = deepcopy(item)
        discounted.price = discounted.price * (1.0 - self._discount_rate)
        return discounted


class FeeBoostStrategy:
    """callable-стратегия вычисления усиленной стоимости доступа"""

    def __init__(self, multiplier: float) -> None:
        if multiplier <= 0.0:
            raise ValueError("multiplier должен быть больше 0")
        self._multiplier = multiplier

    def __call__(self, item: BookItem) -> str:
        boosted = item.calculate_access_fee() * self._multiplier
        return f"{item.title}: boosted_fee={boosted:.2f}₽"

