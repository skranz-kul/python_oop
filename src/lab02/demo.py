"""Демонстрация коллекции Library и модели Book (ЛР-2)."""

from __future__ import annotations

import logging
import sys

from model import Book
from collection import DuplicateBookError, Library, LibraryTypeError

logger = logging.getLogger(__name__)


def _print_library(label: str, library: Library) -> None:
    print(label)
    for book in library:
        print(f"  {book}")
    print()


def scenario_basic_crud() -> None:
    """Сценарий 1: создание книг, добавление, вывод, удаление, повторный вывод."""
    print("=" * 60)
    print("Сценарий 1: базовые операции (add / get_all / remove)")
    print("=" * 60)

    library = Library()
    b1 = Book(
        title="Война и мир",
        author="Лев Толстой",
        year=1873,
        pages=1225,
        price=1500.0,
        inventory_id="INV-L02-001",
    )
    b2 = Book(
        title="Преступление и наказание",
        author="Фёдор Достоевский",
        year=1866,
        pages=672,
        price=900.0,
        inventory_id="INV-L02-002",
    )
    library.add(b1)
    library.add(b2)
    _print_library("После добавления двух книг:", library)

    library.remove(b1)
    print("Удалена первая книга (Война и мир).")
    _print_library("Коллекция после удаления:", library)

    print("Содержимое через get_all():")
    for book in library.get_all():
        print(f"  {book.title} — {book.inventory_id}")
    print()


def scenario_search_len_iter_duplicates() -> None:
    """Сценарий 2: поиск, len, for, ограничение на дубликаты по inventory_id."""
    print("=" * 60)
    print("Сценарий 2: поиск, len(), итерация, запрет дубликатов")
    print("=" * 60)

    library = Library()
    books = [
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
    for book in books:
        library.add(book)

    print(f"len(library) = {len(library)}")
    found = library.find_by_title("Мастер и Маргарита")
    print(f"find_by_title('Мастер и Маргарита'): {len(found)} книг(и)")
    by_id = library.find_by_inventory_id("INV-L02-010")
    print(f"find_by_inventory_id('INV-L02-010'): {by_id.title if by_id else None}")
    print()

    duplicate = Book(
        title="Другая книга",
        author="Другой автор",
        year=2000,
        pages=100,
        price=100.0,
        inventory_id="INV-L02-010",
    )
    try:
        library.add(duplicate)
    except DuplicateBookError as exc:
        logger.warning("Отклонено добавление дубликата: %s", exc)
    print()

    try:
        library.add("not a book")  # type: ignore[arg-type]
    except LibraryTypeError as exc:
        logger.warning("Отклонён неверный тип: %s", exc)
    print()


def scenario_index_sort_filter() -> None:
    """Сценарий 3: индексация, remove_at, сортировка, фильтрация (новая коллекция)."""
    print("=" * 60)
    print("Сценарий 3: индексация, сортировка, фильтрация")
    print("=" * 60)

    library = Library()
    a = Book(
        title="Анна Каренина",
        author="Лев Толстой",
        year=1877,
        pages=864,
        price=1200.0,
        inventory_id="INV-L02-020",
    )
    b = Book(
        title="Евгений Онегин",
        author="Александр Пушкин",
        year=1833,
        pages=320,
        price=400.0,
        inventory_id="INV-L02-021",
    )
    c = Book(
        title="Обломов",
        author="Иван Гончаров",
        year=1859,
        pages=640,
        price=950.0,
        inventory_id="INV-L02-022",
    )
    for book in (a, b, c):
        library.add(book)

    print(f"library[0] = {library[0].title}")
    print(f"library[2] = {library[2].title}")

    anna = library.find_by_inventory_id("INV-L02-020")
    if anna is not None:
        anna.checkout()
        print("Книга «Анна Каренина» выдана (checkout).")
    print()

    available = library.get_available()
    checked_out = library.get_checked_out()
    print("До remove_at: доступные и выданные (новые коллекции):")
    print(f"  get_available(): {len(available)} книг(и)")
    print(f"  get_checked_out(): {len(checked_out)} книг(и)")
    _print_library("  Выданные:", checked_out)
    print()

    removed = library.remove_at(1)
    print(f"remove_at(1) удалил: {removed.title}")
    _print_library("После remove_at:", library)

    library.sort_by_price()
    _print_library("После sort_by_price() (по возрастанию):", library)

    library.sort_by_year(reverse=True)
    _print_library("После sort_by_year(reverse=True):", library)

    available = library.get_available()
    checked_out = library.get_checked_out()
    expensive = library.get_expensive(800.0)

    print("Фильтры возвращают новые объекты Library; исходная коллекция не заменяется:")
    print(f"  len(library) = {len(library)}")
    print(f"  get_available(): {len(available)} книг(и)")
    _print_library("  Доступные:", available)
    print(f"  get_checked_out(): {len(checked_out)} книг(и)")
    _print_library("  Выданные:", checked_out)
    print(f"  get_expensive(800): {len(expensive)} книг(и)")
    _print_library("  Дороже 800:", expensive)
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
