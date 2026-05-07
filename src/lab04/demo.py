from __future__ import annotations

from pathlib import Path
import sys

_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.lab02.collection import Library
from src.lab04.interfaces import Comparable, Printable
from src.lab04.models import AudioBook, Ebook, PrintedBook


def print_all(items: list[Printable]) -> None:
    for item in items:
        print(f"  {item.to_display_string()}")


def sort_by_interface(items: list[Comparable]) -> list[Comparable]:
    return sorted(items, key=lambda item: item.sort_key())


def scenario_interface_calls() -> None:
    print("=" * 70)
    print("сценарий 1: единый список и вызов интерфейсного метода")
    print("=" * 70)

    items: list[Printable] = [
        PrintedBook(
            title="война и мир",
            author="лев толстой",
            year=1873,
            pages=1225,
            price=1500.0,
            inventory_id="INV-L04-001",
            cover_type="hard",
            print_run=5000,
        ),
        Ebook(
            title="clean architecture",
            author="robert martin",
            year=2017,
            pages=432,
            price=1400.0,
            inventory_id="INV-L04-002",
            file_format="pdf",
            file_size_mb=5.8,
        ),
        AudioBook(
            title="1984",
            author="george orwell",
            year=1949,
            pages=328,
            price=900.0,
            inventory_id="INV-L04-003",
            duration_minutes=680,
            narrator="simon prebble",
        ),
    ]
    print_all(items)
    print()


def scenario_universal_functions() -> None:
    print("=" * 70)
    print("сценарий 2: универсальные функции и isinstance")
    print("=" * 70)

    mixed: list[Comparable] = [
        PrintedBook(
            title="мастер и маргарита",
            author="михаил булгаков",
            year=1967,
            pages=512,
            price=800.0,
            inventory_id="INV-L04-010",
            cover_type="soft",
            print_run=3000,
        ),
        Ebook(
            title="domain-driven design",
            author="eric evans",
            year=2003,
            pages=560,
            price=2200.0,
            inventory_id="INV-L04-011",
            file_format="epub",
            file_size_mb=18.0,
        ),
        AudioBook(
            title="герой нашего времени",
            author="м. лермонтов",
            year=1840,
            pages=256,
            price=600.0,
            inventory_id="INV-L04-012",
            duration_minutes=410,
            narrator="игорь князев",
        ),
    ]

    sorted_items = sort_by_interface(mixed)
    print("после sort_by_interface:")
    for item in sorted_items:
        # на практике работает полиморфно через интерфейс comparable
        print(f"  key={item.sort_key()}")
    print()

    print("проверка isinstance по интерфейсам:")
    for item in mixed:
        print(
            f"  {item.__class__.__name__}: "
            f"printable={isinstance(item, Printable)}, "
            f"comparable={isinstance(item, Comparable)}"
        )
    print()


def scenario_collection_integration() -> None:
    print("=" * 70)
    print("сценарий 3: интеграция с library и фильтрация по интерфейсу")
    print("=" * 70)

    library = Library()
    objects = [
        PrintedBook(
            title="анна каренина",
            author="лев толстой",
            year=1877,
            pages=864,
            price=1200.0,
            inventory_id="INV-L04-020",
            cover_type="hard",
            print_run=2500,
        ),
        Ebook(
            title="refactoring",
            author="martin fowler",
            year=2018,
            pages=448,
            price=1800.0,
            inventory_id="INV-L04-021",
            file_format="pdf",
            file_size_mb=12.4,
        ),
        AudioBook(
            title="обломов",
            author="иван гончаров",
            year=1859,
            pages=640,
            price=700.0,
            inventory_id="INV-L04-022",
            duration_minutes=520,
            narrator="александр клюквин",
        ),
    ]
    for obj in objects:
        library.add(obj)

    printable_items = library.get_printable()
    comparable_items = library.get_comparable()

    print("выборка get_printable():")
    print_all(printable_items)
    print()

    print("выборка get_comparable() и сортировка:")
    for item in sort_by_interface(comparable_items):
        print(f"  {item.sort_key()}")
    print()


def main() -> None:
    scenario_interface_calls()
    scenario_universal_functions()
    scenario_collection_integration()
    print("демонстрация лр-4 завершена")


if __name__ == "__main__":
    main()

