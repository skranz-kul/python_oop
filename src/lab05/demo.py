from __future__ import annotations

from pathlib import Path
import sys

_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.lab04.models import AudioBook, Ebook, PrintedBook
from src.lab05.collection import BookCollection
from src.lab05.strategies import (
    DiscountStrategy,
    FeeBoostStrategy,
    by_multi,
    by_price,
    by_title,
    is_ebook,
    is_expensive,
    make_max_price_filter,
    to_summary,
    to_title,
)


def _print_items(label: str, items: BookCollection[object]) -> None:
    print(label)
    for item in items:
        print(f"  {item}")
    print()


def _seed_collection() -> BookCollection[PrintedBook | Ebook | AudioBook]:
    items = [
        PrintedBook(
            title="война и мир",
            author="лев толстой",
            year=1873,
            pages=1225,
            price=1500.0,
            inventory_id="INV-L05-001",
            cover_type="hard",
            print_run=5000,
        ),
        Ebook(
            title="clean architecture",
            author="robert martin",
            year=2017,
            pages=432,
            price=1400.0,
            inventory_id="INV-L05-002",
            file_format="pdf",
            file_size_mb=5.8,
        ),
        AudioBook(
            title="1984",
            author="george orwell",
            year=1949,
            pages=328,
            price=900.0,
            inventory_id="INV-L05-003",
            duration_minutes=680,
            narrator="simon prebble",
        ),
        Ebook(
            title="domain-driven design",
            author="eric evans",
            year=2003,
            pages=560,
            price=2200.0,
            inventory_id="INV-L05-004",
            file_format="epub",
            file_size_mb=18.0,
        ),
        PrintedBook(
            title="мастер и маргарита",
            author="михаил булгаков",
            year=1967,
            pages=512,
            price=800.0,
            inventory_id="INV-L05-005",
            cover_type="soft",
            print_run=3000,
        ),
    ]
    return BookCollection(items)


def scenario_chain_filter_sort_apply() -> None:
    print("=" * 70)
    print("сценарий 1: полная цепочка filter -> sort -> apply")
    print("=" * 70)
    collection = _seed_collection()
    _print_items("исходная коллекция:", BookCollection(collection.to_list()))

    filtered = collection.filter_by(lambda item: is_expensive(item, min_price=1000.0))
    _print_items("после filter_by (price >= 1000):", BookCollection(filtered.to_list()))

    sorted_collection = filtered.sort_by(by_price)
    _print_items("после sort_by(by_price):", BookCollection(sorted_collection.to_list()))

    summaries = sorted_collection.apply(to_summary)
    _print_items("после apply(to_summary):", BookCollection(summaries.to_list()))


def scenario_replace_strategies() -> None:
    print("=" * 70)
    print("сценарий 2: замена стратегии без изменения кода коллекции")
    print("=" * 70)
    collection = _seed_collection()

    by_title_result = collection.sort_by(by_title)
    _print_items("сортировка стратегией by_title:", BookCollection(by_title_result.to_list()))

    by_multi_result = collection.sort_by(by_multi)
    _print_items("сортировка стратегией by_multi:", BookCollection(by_multi_result.to_list()))

    only_ebooks_named = collection.filter_by(is_ebook)
    only_ebooks_lambda = collection.filter_by(lambda item: isinstance(item, Ebook))
    _print_items("фильтрация is_ebook:", BookCollection(only_ebooks_named.to_list()))
    _print_items("фильтрация lambda isinstance(..., Ebook):", BookCollection(only_ebooks_lambda.to_list()))

    names_via_map = list(map(to_title, collection))
    names_via_lambda = list(map(lambda item: item.title, collection))
    print("map через именованную функцию:", names_via_map)
    print("map через lambda:", names_via_lambda)
    print()

    max_1200_filter = make_max_price_filter(1200.0)
    filtered = collection.filter_by(max_1200_filter)
    _print_items("фабрика фильтра make_max_price_filter(1200):", BookCollection(filtered.to_list()))

    filtered_builtin = filter(max_1200_filter, collection)
    print("результат встроенного filter(...):")
    print(filtered_builtin)
    for item in filtered_builtin:
        print(f"  {item}")
    print()


def scenario_callable_object_strategy() -> None:
    print("=" * 70)
    print("сценарий 3: callable-объект как стратегия")
    print("=" * 70)
    collection = _seed_collection()

    discount_strategy = DiscountStrategy(0.15)
    discounted = collection.apply(discount_strategy)
    _print_items("после apply(DiscountStrategy(0.15)):", BookCollection(discounted.to_list()))

    fee_strategy = FeeBoostStrategy(1.2)
    boosted_fees = collection.apply(fee_strategy)
    _print_items("после apply(FeeBoostStrategy(1.2)):", BookCollection(boosted_fees.to_list()))


def main() -> None:
    scenario_chain_filter_sort_apply()
    scenario_replace_strategies()
    scenario_callable_object_strategy()
    print("демонстрация лр-5 завершена")


if __name__ == "__main__":
    main()

