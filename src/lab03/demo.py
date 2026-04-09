"""Демонстрация ЛР-3: наследование, полиморфизм, коллекция."""

from __future__ import annotations


from src.lab02.collection import Library
from .base import Book
from .models import AudioBook, Ebook, PrintedBook


def _print_collection(label: str, collection: Library) -> None:
    print(label)
    for item in collection:
        print(f"  {item}")
    print()


def scenario_inheritance_and_methods() -> None:
    print("=" * 70)
    print("Сценарий 1: наследование и методы дочерних классов")
    print("=" * 70)

    printed = PrintedBook(
        title="Война и мир",
        author="Лев Толстой",
        year=1873,
        pages=1225,
        price=1500.0,
        inventory_id="INV-L03-001",
        cover_type="hard",
        print_run=5000,
    )
    ebook = Ebook(
        title="Чистый код",
        author="Robert Martin",
        year=2008,
        pages=464,
        price=1200.0,
        inventory_id="INV-L03-002",
        file_format="epub",
        file_size_mb=3.2,
    )
    audio = AudioBook(
        title="1984",
        author="George Orwell",
        year=1949,
        pages=328,
        price=950.0,
        inventory_id="INV-L03-003",
        duration_minutes=680,
        narrator="Simon Prebble",
    )

    print(printed)
    print(f"  Метод потомка estimate_restoration_cost: {printed.estimate_restoration_cost()}")
    print(ebook)
    print(f"  Метод потомка download_link: {ebook.download_link()}")
    print(audio)
    print(f"  Метод потомка sample_seconds: {audio.sample_seconds()}")
    print()


def scenario_polymorphism_and_isinstance() -> None:
    print("=" * 70)
    print("Сценарий 2: полиморфизм и isinstance()")
    print("=" * 70)

    items: list[Book] = [
        PrintedBook(
            title="Преступление и наказание",
            author="Ф. Достоевский",
            year=1866,
            pages=672,
            price=900.0,
            inventory_id="INV-L03-010",
            cover_type="soft",
            print_run=3500,
        ),
        Ebook(
            title="Refactoring",
            author="Martin Fowler",
            year=2018,
            pages=448,
            price=1800.0,
            inventory_id="INV-L03-011",
            file_format="pdf",
            file_size_mb=12.4,
        ),
        AudioBook(
            title="Мастер и Маргарита",
            author="М. Булгаков",
            year=1967,
            pages=512,
            price=700.0,
            inventory_id="INV-L03-012",
            duration_minutes=760,
            narrator="Алексей Багдасаров",
        ),
    ]

    print("Единый список list[Book], один вызов calculate_access_fee(), разное поведение:")
    for obj in items:
        print(f"  {obj.__class__.__name__}: fee = {obj.calculate_access_fee():.2f}₽")

    print("\nПроверка типов через isinstance():")
    for obj in items:
        if isinstance(obj, Ebook):
            print(f"  {obj.title} -> Ebook, формат: {obj.file_format}")
        elif isinstance(obj, AudioBook):
            print(f"  {obj.title} -> AudioBook, диктор: {obj.narrator}")
        elif isinstance(obj, PrintedBook):
            print(f"  {obj.title} -> PrintedBook, обложка: {obj.cover_type}")
    print()


def scenario_collection_integration() -> None:
    print("=" * 70)
    print("Сценарий 3: интеграция с Library и фильтрация по типам")
    print("=" * 70)

    collection = Library()
    mixed_items: list[Book] = [
        PrintedBook(
            title="Анна Каренина",
            author="Лев Толстой",
            year=1877,
            pages=864,
            price=1200.0,
            inventory_id="INV-L03-020",
            cover_type="hard",
            print_run=2000,
        ),
        Ebook(
            title="Domain-Driven Design",
            author="Eric Evans",
            year=2003,
            pages=560,
            price=2200.0,
            inventory_id="INV-L03-021",
            file_format="pdf",
            file_size_mb=18.0,
        ),
        AudioBook(
            title="Герой нашего времени",
            author="М. Лермонтов",
            year=1840,
            pages=256,
            price=600.0,
            inventory_id="INV-L03-022",
            duration_minutes=410,
            narrator="Игорь Князев",
        ),
    ]
    for item in mixed_items:
        collection.add(item)

    _print_collection("Смешанная коллекция (разные типы в одном контейнере):", collection)

    ebooks = collection.get_only_ebooks()
    audio_books = collection.get_only_audio_books()
    printed = collection.get_only_printed()
    _print_collection("Только Ebook:", ebooks)
    _print_collection("Только AudioBook:", audio_books)
    _print_collection("Только PrintedBook:", printed)


def main() -> None:
    scenario_inheritance_and_methods()
    scenario_polymorphism_and_isinstance()
    scenario_collection_integration()
    print("Демонстрация ЛР-3 завершена.")


if __name__ == "__main__":
    main()

