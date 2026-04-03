"""Демонстрация коллекции Library и модели Book (ЛР-2)."""

from __future__ import annotations

import logging
import sys

from model import Book
from collection import DuplicateBookError, Library, LibraryTypeError

logger = logging.getLogger(__name__)


def _print_library(label: str, collection: Library) -> None:
    print(label)
    for book in collection:
        print(f"  {book}")
    print()


def scenario_basic_crud() -> None:
    """Сценарий 1: создание книг, добавление, вывод, удаление, повторный вывод."""
    print("=" * 60)
    print("Сценарий 1: базовые операции (add / get_all / remove)")
    print("=" * 60)

    catalog = Library()
    war_and_peace = Book(
        title="Война и мир",
        author="Лев Толстой",
        year=1873,
        pages=1225,
        price=1500.0,
        inventory_id="INV-L02-001",
    )
    crime_and_punishment = Book(
        title="Преступление и наказание",
        author="Фёдор Достоевский",
        year=1866,
        pages=672,
        price=900.0,
        inventory_id="INV-L02-002",
    )
    catalog.add(war_and_peace)
    catalog.add(crime_and_punishment)
    _print_library("После добавления двух книг:", catalog)

    catalog.remove(war_and_peace)
    print("Удалена первая книга (Война и мир).")
    _print_library("Коллекция после удаления:", catalog)

    print("Содержимое через get_all():")
    for book in catalog.get_all():
        print(f"  {book.title} — {book.inventory_id}")
    print()


def scenario_search_len_iter_duplicates() -> None:
    """Сценарий 2: поиск, len, for, ограничение на дубликаты по inventory_id."""
    print("=" * 60)
    print("Сценарий 2: поиск, len(), итерация, запрет дубликатов")
    print("=" * 60)

    catalog = Library()
    margarita_editions = [
        Book(
            title="Мастер и Маргарита",
            author="Михаил Булгаков",
            year=1967,
            pages=672,
            price=750.0,
            inventory_id="INV-L02-010",
        ),
        Book(
            title="Мастер и Маргарита",
            author="Михаил Булгаков",
            year=1990,
            pages=512,
            price=500.0,
            inventory_id="INV-L02-011",
        ),
    ]
    for book in margarita_editions:
        catalog.add(book)

    print(f"len(catalog) = {len(catalog)}")
    same_title = catalog.find_by_title("Мастер и Маргарита")
    print(f"find_by_title('Мастер и Маргарита'): {len(same_title)} книг(и)")
    lookup_inv = catalog.find_by_inventory_id("INV-L02-010")
    print(f"find_by_inventory_id('INV-L02-010'): {lookup_inv.title if lookup_inv else None}")
    print()

    inv_id_collision = Book(
        title="Другая книга",
        author="Другой автор",
        year=2000,
        pages=100,
        price=100.0,
        inventory_id="INV-L02-010",
    )
    try:
        catalog.add(inv_id_collision)
    except DuplicateBookError as exc:
        logger.warning("Отклонено добавление дубликата: %s", exc)
    print()

    try:
        catalog.add("not a book")  # type: ignore[arg-type]
    except LibraryTypeError as exc:
        logger.warning("Отклонён неверный тип: %s", exc)
    print()


def scenario_index_sort_filter() -> None:
    """Сценарий 3: индексация, remove_at, сортировка, фильтрация (новая коллекция)."""
    print("=" * 60)
    print("Сценарий 3: индексация, сортировка, фильтрация")
    print("=" * 60)

    catalog = Library()
    anna_karenina = Book(
        title="Анна Каренина",
        author="Лев Толстой",
        year=1877,
        pages=864,
        price=1200.0,
        inventory_id="INV-L02-020",
    )
    evgeny_onegin = Book(
        title="Евгений Онегин",
        author="Александр Пушкин",
        year=1833,
        pages=320,
        price=400.0,
        inventory_id="INV-L02-021",
    )
    oblomov = Book(
        title="Обломов",
        author="Иван Гончаров",
        year=1859,
        pages=640,
        price=950.0,
        inventory_id="INV-L02-022",
    )
    for book in (anna_karenina, evgeny_onegin, oblomov):
        catalog.add(book)

    print(f"catalog[0] = {catalog[0].title}")
    print(f"catalog[2] = {catalog[2].title}")

    anna_book = catalog.find_by_inventory_id("INV-L02-020")
    if anna_book is not None:
        anna_book.checkout()
        print("Книга «Анна Каренина» выдана (checkout).")
    print()

    on_shelf = catalog.get_available()
    on_loan = catalog.get_checked_out()
    print("До remove_at: доступные и выданные (новые коллекции):")
    print(f"  get_available(): {len(on_shelf)} книг(и)")
    print(f"  get_checked_out(): {len(on_loan)} книг(и)")
    _print_library("  Выданные:", on_loan)
    print()

    popped = catalog.remove_at(1)
    print(f"remove_at(1) удалил: {popped.title}")
    _print_library("После remove_at:", catalog)

    catalog.sort_by_price()
    _print_library("После sort_by_price() (по возрастанию):", catalog)

    catalog.sort_by_year(reverse=True)
    _print_library("После sort_by_year(reverse=True):", catalog)

    on_shelf = catalog.get_available()
    on_loan = catalog.get_checked_out()
    pricey = catalog.get_expensive(800.0)

    print("Фильтры возвращают новые объекты Library; исходная коллекция не заменяется:")
    print(f"  len(catalog) = {len(catalog)}")
    print(f"  get_available(): {len(on_shelf)} книг(и)")
    _print_library("  Доступные:", on_shelf)
    print(f"  get_checked_out(): {len(on_loan)} книг(и)")
    _print_library("  Выданные:", on_loan)
    print(f"  get_expensive(800): {len(pricey)} книг(и)")
    _print_library("  Дороже 800:", pricey)
    print()


def main() -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format="WARNING: %(message)s",
        stream=sys.stdout,
        force=True,
    )
    scenario_basic_crud()
    scenario_search_len_iter_duplicates()
    scenario_index_sort_filter()
    print("Демонстрация завершена.")


if __name__ == "__main__":
    main()
