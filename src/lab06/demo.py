"""Демонстрация ЛР-6: TypedCollection, TypeVar, Protocol."""

from __future__ import annotations

import logging
from pathlib import Path
import sys

_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

from src.lab06.container import (
    D,
    LibraryItem,
    LibraryTypeError,
    S,
    TypedCollection,
)
from src.lab03.models import AudioBook, PrintedBook

logger = logging.getLogger(__name__)


def scenario_typed_collection_and_runtime_validation() -> None:
    print("=== Сценарий 1 (оценка 3): коллекция LibraryItem и проверка типа при add ===\n")
    books: TypedCollection[LibraryItem] = TypedCollection(
        allowed_item_type=TypedCollection.default_library_book_types(),
    )
    printed = PrintedBook(
        title="война и мир",
        author="лев толстой",
        year=1873,
        pages=1225,
        price=1500.0,
        inventory_id="INV-L06-001",
        cover_type="hard",
        print_run=3000,
    )
    audio = AudioBook(
        title="1984",
        author="george orwell",
        year=1949,
        pages=328,
        price=900.0,
        inventory_id="INV-L06-002",
        duration_minutes=600,
        narrator="john hurt",
    )
    books.add(printed)
    books.add(audio)
    print("Все элементы:")
    for item in books.get_all():
        print(f"  {item}")
    print()

    print("Попытка добавить объект неподходящего типа (dict):")
    try:
        books.add({"not": "a book"})  # type: ignore[arg-type]
    except LibraryTypeError as err:
        print(f"  Поймано ожидаемое исключение: {err}")
    print()


def scenario_find_filter_map() -> None:
    print("=== Сценарий 2 (оценка 4): find, filter, map ===\n")
    books: TypedCollection[LibraryItem] = TypedCollection(
        allowed_item_type=TypedCollection.default_library_book_types(),
    )
    books.add(
        PrintedBook(
            title="мастер и маргарита",
            author="михаил булгаков",
            year=1967,
            pages=480,
            price=700.0,
            inventory_id="INV-L06-010",
            cover_type="soft",
            print_run=1200,
        )
    )
    books.add(
        AudioBook(
            title="мастер и маргарита",
            author="михаил булгаков",
            year=2010,
            pages=1,
            price=500.0,
            inventory_id="INV-L06-011",
            duration_minutes=800,
            narrator="unknown",
        )
    )
    books.add(
        PrintedBook(
            title="чистая архитектура",
            author="robert martin",
            year=2017,
            pages=432,
            price=1400.0,
            inventory_id="INV-L06-012",
            cover_type="hard",
            print_run=2000,
        )
    )

    found = books.find(lambda b: b.inventory_id == "INV-L06-011")
    print(f"find по инвентарному номеру: найдено -> {found}")
    missing = books.find(lambda b: b.inventory_id == "INV-9999")
    print(f"find: не найдено -> {missing!r}")
    print()

    filtered = books.filter(lambda b: b.price >= 500.0)
    print(f"filter (цена >= 500): {len(filtered)} шт.")
    for b in filtered:
        print(f"  {b.title!r} — {b.price:.2f}₽")
    print()

    titles: list[str] = books.map(lambda b: b.title)
    print(f"map -> list[str] (заголовки): {titles}")
    scores: list[float] = books.map(lambda b: b.score())
    print(f"map -> list[float] (score): {scores}")
    print()


def scenario_protocol_displayable() -> None:
    print("=== Сценарий 3а (оценка 5): TypedCollection[D], разные классы ЛР-3 ===\n")
    books: TypedCollection[D] = TypedCollection(
        allowed_item_type=(PrintedBook, AudioBook),
    )
    books.add(
        PrintedBook(
            title="преступление и наказание",
            author="фёдор достоевский",
            year=1866,
            pages=672,
            price=900.0,
            inventory_id="INV-L06-D1",
            cover_type="hard",
            print_run=4000,
        )
    )
    books.add(
        AudioBook(
            title="идиот",
            author="фёдор достоевский",
            year=1869,
            pages=600,
            price=800.0,
            inventory_id="INV-L06-D2",
            duration_minutes=900,
            narrator="artist",
        )
    )
    print("Классы не наследуют Displayable — вызываем item.display():")
    for item in books.get_all():
        print(f"  {type(item).__name__}: {item.display()}")
    print()


def scenario_protocol_scorable() -> None:
    print("=== Сценарий 3б (оценка 5): TypedCollection[S], тот же TypedCollection ===\n")
    scored: TypedCollection[S] = TypedCollection(
        allowed_item_type=(PrintedBook, AudioBook),
    )
    scored.add(
        PrintedBook(
            title="анна каренина",
            author="лев толстой",
            year=1878,
            pages=864,
            price=1100.0,
            inventory_id="INV-L06-S1",
            cover_type="soft",
            print_run=2500,
        )
    )
    scored.add(
        AudioBook(
            title="воскресение",
            author="лев толстой",
            year=1899,
            pages=522,
            price=650.0,
            inventory_id="INV-L06-S2",
            duration_minutes=700,
            narrator="reader",
        )
    )
    print("Тот же класс контейнера, другое ограничение TypeVar (bound=Scorable):")
    for item in scored.get_all():
        print(f"  {type(item).__name__}: score={item.score():.2f}")
    print()


def main() -> None:
    scenario_typed_collection_and_runtime_validation()
    scenario_find_filter_map()
    scenario_protocol_displayable()
    scenario_protocol_scorable()
    logger.info("Демонстрация ЛР-6 завершена.")


if __name__ == "__main__":
    main()
