from __future__ import annotations

from src.lab03.base import Book as Lab03Book
from src.lab03.models import AudioBook as Lab03AudioBook
from src.lab03.models import Ebook as Lab03Ebook
from src.lab03.models import PrintedBook as Lab03PrintedBook
from src.lab04.interfaces import Comparable, Printable


class Book(Lab03Book, Printable, Comparable):
    def to_display_string(self) -> str:
        return (
            f"book: {self.title} | {self.author} | {self.year} | "
            f"{self.price:.2f}₽ | {self.state}"
        )

    def sort_key(self) -> tuple[object, ...]:
        return (self.title, self.author, self.year, self.price)


class PrintedBook(Lab03PrintedBook, Printable, Comparable):
    def to_display_string(self) -> str:
        return (
            f"printed: {self.title} | cover={self.cover_type} | run={self.print_run} | "
            f"fee={self.calculate_access_fee():.2f}₽"
        )

    def sort_key(self) -> tuple[object, ...]:
        return (self.title, self.print_run, self.price)


class Ebook(Lab03Ebook, Printable, Comparable):
    def to_display_string(self) -> str:
        return (
            f"ebook: {self.title} | {self.file_format} | {self.file_size_mb:.2f}mb | "
            f"fee={self.calculate_access_fee():.2f}₽"
        )

    def sort_key(self) -> tuple[object, ...]:
        return (self.title, self.file_format, self.file_size_mb, self.price)


class AudioBook(Lab03AudioBook, Printable, Comparable):
    def to_display_string(self) -> str:
        return (
            f"audio: {self.title} | narrator={self.narrator} | "
            f"{self.duration_minutes}min | fee={self.calculate_access_fee():.2f}₽"
        )

    def sort_key(self) -> tuple[object, ...]:
        return (self.title, self.duration_minutes, self.price)


__all__ = (
    "AudioBook",
    "Book",
    "Comparable",
    "Ebook",
    "Printable",
    "PrintedBook",
)

