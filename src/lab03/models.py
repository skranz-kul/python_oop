from __future__ import annotations

try:
    from ..lib.book_validators import (
        validate_float_min,
        validate_int_min,
        validate_non_empty_string,
    )
    from .base import Book, BookValidationError
except ImportError:
    from lib.book_validators import (  # type: ignore[no-redef]
        validate_float_min,
        validate_int_min,
        validate_non_empty_string,
    )
    from lab03.base import Book, BookValidationError  # type: ignore[no-redef]


class PrintedBook(Book):
    """Печатная книга."""

    ALLOWED_COVER_TYPES: tuple[str, ...] = ("soft", "hard")

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        pages: int,
        price: float,
        inventory_id: str,
        cover_type: str,
        print_run: int,
        state: str = "available",
    ) -> None:
        super().__init__(title, author, year, pages, price, inventory_id, state)
        self._cover_type: str = self._validate_cover_type(cover_type)
        self._print_run: int = validate_int_min(
            print_run,
            1,
            "Тираж",
            BookValidationError,
        )

    @property
    def cover_type(self) -> str:
        return self._cover_type

    @property
    def print_run(self) -> int:
        return self._print_run

    def _validate_cover_type(self, value: str) -> str:
        normalized = validate_non_empty_string(value, "Тип обложки", BookValidationError)
        if normalized not in self.ALLOWED_COVER_TYPES:
            allowed = ", ".join(self.ALLOWED_COVER_TYPES)
            raise BookValidationError(
                f"Недопустимый тип обложки {normalized!r}. Разрешено: {allowed}."
            )
        return normalized

    def calculate_access_fee(self) -> float:
        """Печатная книга дороже в обработке (выдача + износ)."""
        return round(self.price + 80.0, 2)

    def estimate_restoration_cost(self) -> float:
        return round(self.pages * 0.35, 2)

    def __str__(self) -> str:
        return (
            f"PrintedBook '{self.title}' ({self.cover_type} cover, run={self.print_run}) "
            f"[{self.inventory_id}] fee={self.calculate_access_fee():.2f}₽"
        )


class Ebook(Book):
    """Электронная книга."""

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        pages: int,
        price: float,
        inventory_id: str,
        file_format: str,
        file_size_mb: float,
        state: str = "available",
    ) -> None:
        super().__init__(title, author, year, pages, price, inventory_id, state)
        self._file_format: str = validate_non_empty_string(
            file_format,
            "Формат файла",
            BookValidationError,
        ).lower()
        self._file_size_mb: float = validate_float_min(
            file_size_mb,
            0.1,
            "Размер файла",
            BookValidationError,
        )

    @property
    def file_format(self) -> str:
        return self._file_format

    @property
    def file_size_mb(self) -> float:
        return self._file_size_mb

    def download_link(self) -> str:
        return f"https://library.local/download/{self.inventory_id}.{self.file_format}"

    def calculate_access_fee(self) -> float:
        """Для Ebook стоимость доступа меньше физического экземпляра."""
        return round(self.price * 0.35, 2)

    def __str__(self) -> str:
        return (
            f"Ebook '{self.title}' ({self.file_format}, {self.file_size_mb:.2f}MB) "
            f"[{self.inventory_id}] fee={self.calculate_access_fee():.2f}₽"
        )


class AudioBook(Book):
    """Аудиокнига."""

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        pages: int,
        price: float,
        inventory_id: str,
        duration_minutes: int,
        narrator: str,
        state: str = "available",
    ) -> None:
        super().__init__(title, author, year, pages, price, inventory_id, state)
        self._duration_minutes: int = validate_int_min(
            duration_minutes,
            1,
            "Длительность",
            BookValidationError,
        )
        self._narrator: str = validate_non_empty_string(
            narrator,
            "Диктор",
            BookValidationError,
        )

    @property
    def duration_minutes(self) -> int:
        return self._duration_minutes

    @property
    def narrator(self) -> str:
        return self._narrator

    def sample_seconds(self) -> int:
        return min(120, self.duration_minutes * 60 // 10)

    def calculate_access_fee(self) -> float:
        """Учитываем базовую цену и длину аудио."""
        return round(self.price * 0.5 + self.duration_minutes * 0.2, 2)

    def __str__(self) -> str:
        return (
            f"AudioBook '{self.title}' (narrator={self.narrator}, "
            f"duration={self.duration_minutes}min) "
            f"[{self.inventory_id}] fee={self.calculate_access_fee():.2f}₽"
        )

