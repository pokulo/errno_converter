import abc
from typing import Sequence


class Converter(object, metaclass=abc.ABCMeta):
    NAME: str = ""
    NUMBER_RANGE: Sequence[int] = ()

    @staticmethod
    @abc.abstractmethod
    def number2code(number: int) -> str:
        """Convert a single numerical code to its textual code, raise an Exception if impossible."""

    @staticmethod
    @abc.abstractmethod
    def code2number(code: str) -> int:
        """Convert a textual code to its numerical code, raise an Exception if impossible."""

    @staticmethod
    @abc.abstractmethod
    def number2description(number: int) -> str:
        """Convert a numerical code to its description (empty string if impossible)"""

    @staticmethod
    @abc.abstractmethod
    def get_candidates() -> list[str]:
        """List all textual codes that can be converted."""
