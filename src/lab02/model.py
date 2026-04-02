"""Модель предметной области ЛР-2: реэкспорт сущности `Book` из ЛР-1."""

from __future__ import annotations

try:
    from ..lab01.model import Book, BookState, BookValidationError
except ImportError:
    from pathlib import Path
    import sys

    _src = Path(__file__).resolve().parent.parent
    if str(_src) not in sys.path:
        sys.path.insert(0, str(_src))
    from lab01.model import Book, BookState, BookValidationError

__all__ = ("Book", "BookState", "BookValidationError")
