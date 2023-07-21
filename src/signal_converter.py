import signal
from typing import Sequence

from lib.converter import Converter
from lib.parser import Parser


class SignalConverter(Converter):
    NAME: str = "signal"
    NUMBER_RANGE: Sequence[int] = range(1, 65)

    @staticmethod
    def number2code(number: int) -> str:
        return signal.Signals(int(number)).name

    @staticmethod
    def code2number(code: str) -> int:
        return getattr(signal, code).value

    @staticmethod
    def get_candidates() -> list[str]:
        return dir(signal)

    @staticmethod
    def number2description(number: int) -> str:
        return signal.strsignal(signal.Signals(int(number))) or ""


def main() -> None:
    return Parser.parse(SignalConverter)
