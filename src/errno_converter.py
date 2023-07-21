import os
import errno

from converter_lib import Converter, Parser


class ErrnoConverter(Converter):
    NAME: str = "errno"
    NUMBER_RANGE: range = range(1, 132)

    @staticmethod
    def number2code(number: int) -> str:
        return errno.errorcode[int(number)]

    @staticmethod
    def code2number(code: str) -> int:
        return getattr(errno, code)

    @staticmethod
    def get_candidates() -> list[str]:
        return dir(errno)

    @staticmethod
    def number2description(number: int) -> str:
        return os.strerror(number)


def main() -> None:
    return Parser.parse(ErrnoConverter)
