from __future__ import annotations

from abc import ABC, abstractmethod


class Printable(ABC):
    @abstractmethod
    def to_display_string(self) -> str:
        raise NotImplementedError


class Comparable(ABC):
    @abstractmethod
    def sort_key(self) -> tuple[object, ...]:
        raise NotImplementedError

