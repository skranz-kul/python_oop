from __future__ import annotations

from model import Book, BookState, BookValidationError


def scenario_creation_and_output() -> None:
    print("=== Сценарий 1: корректное создание и вывод ===")
    book = Book(
        title="Война и мир",
        author="Лев Толстой",
        year=1873,
        pages=1225,
        price=1500.0,
        inventory_id="INV-0001",
    )
    print(book)
    print(repr(book))
    print()


def scenario_equality() -> None:
    print("=== Сценарий 2: сравнение объектов ===")
    first = Book(
        title="Преступление и наказание",
        author="Фёдор Достоевский",
        year=1866,
        pages=672,
        price=900.0,
        inventory_id="INV-0002",
    )
    same_inventory = Book(
        title="Преступление и наказание (другое издание)",
        author="Фёдор Достоевский",
        year=2000,
        pages=700,
        price=1200.0,
        inventory_id="INV-0002",
    )
    different = Book(
        title="Идиот",
        author="Фёдор Достоевский",
        year=1869,
        pages=600,
        price=800.0,
        inventory_id="INV-0003",
    )

    print(f"first == same_inventory: {first == same_inventory}")
    print(f"first == different: {first == different}")
    print()


def scenario_invalid_creation() -> None:
    print("=== Сценарий 3: ошибочная инициализация ===")
    invalid_cases = [
        dict(
            title="",
            author="Автор",
            year=2000,
            pages=100,
            price=500.0,
            inventory_id="INV-1001",
        ),
        dict(
            title="Некорректный год",
            author="Автор",
            year=1400,
            pages=100,
            price=500.0,
            inventory_id="INV-1002",
        ),
        dict(
            title="Отрицательная цена",
            author="Автор",
            year=2000,
            pages=100,
            price=-10.0,
            inventory_id="INV-1003",
        ),
        dict(
            title="Нулевые страницы",
            author="Автор",
            year=2000,
            pages=0,
            price=500.0,
            inventory_id="INV-1004",
        ),
    ]

    for index, params in enumerate(invalid_cases, start=1):
        try:
            print(f"Пробуем создать некорректную книгу #{index} ...")
            Book(**params)
        except BookValidationError as error:
            print(f"Ожидаемая ошибка: {error}")
    print()


def scenario_price_setter() -> None:
    print("=== Сценарий 4: setter и ограничения ===")
    book = Book(
        title="Мастер и Маргарита",
        author="Михаил Булгаков",
        year=1967,
        pages=480,
        price=700.0,
        inventory_id="INV-2001",
    )
    print(f"Исходная цена: {book.price:.2f}₽")
    book.price = 850.5
    print(f"Новая цена: {book.price:.2f}₽")

    try:
        print("Пробуем установить отрицательную цену ...")
        book.price = -100.0
    except BookValidationError as error:
        print(f"Ожидаемая ошибка: {error}")
    print()


def scenario_class_attributes() -> None:
    print("=== Сценарий 5: атрибуты класса ===")
    print(f"Допустимые состояния книги (через класс): {Book.ALLOWED_STATES}")
    book = Book(
        title="Анна Каренина",
        author="Лев Толстой",
        year=1878,
        pages=864,
        price=1100.0,
        inventory_id="INV-3001",
    )
    print(f"Допустимые состояния (через экземпляр): {book.ALLOWED_STATES}")
    print(f"Минимальный год издания: {Book.MIN_YEAR}")
    print(f"Максимальный год издания: {Book.MAX_YEAR}")
    print()


def scenario_states_and_transitions() -> None:
    print("=== Сценарий 6: логические состояния и поведение ===")

    # Нормальный сценарий: available -> checked_out -> available
    print("--- Нормальный сценарий ---")
    normal = Book(
        title="Нормальный сценарий",
        author="Автор",
        year=2000,
        pages=300,
        price=500.0,
        inventory_id="INV-4001",
    )
    print(normal)
    normal.checkout()
    print(f"После checkout: state={normal.state}")
    normal.return_book()
    print(f"После return_book: state={normal.state}")
    print()

    # Нарушение ограничения: повторный checkout
    print("--- Сценарий с нарушением ограничения ---")
    invalid_checkout = Book(
        title="Повторная выдача",
        author="Автор",
        year=2001,
        pages=250,
        price=400.0,
        inventory_id="INV-4002",
    )
    invalid_checkout.checkout()
    print(f"После первого checkout: state={invalid_checkout.state}")
    try:
        print("Пробуем выдать книгу повторно ...")
        invalid_checkout.checkout()
    except BookValidationError as error:
        print(f"Ожидаемая ошибка: {error}")
    print()

    # Сценарий со сменой состояния на утерянную
    print("--- Сценарий с утерянной книгой ---")
    lost_book = Book(
        title="Утерянная книга",
        author="Автор",
        year=1999,
        pages=200,
        price=300.0,
        inventory_id="INV-4003",
    )
    print(f"Начальное состояние: {lost_book.state}")
    lost_book.mark_lost()
    print(f"После mark_lost: state={lost_book.state}")
    try:
        print("Пробуем выдать утерянную книгу ...")
        lost_book.checkout()
    except BookValidationError as error:
        print(f"Ожидаемая ошибка: {error}")
    print()


def main() -> None:
    scenario_creation_and_output()
    scenario_equality()
    scenario_invalid_creation()
    scenario_price_setter()
    scenario_class_attributes()
    scenario_states_and_transitions()


if __name__ == "__main__":
    main()

