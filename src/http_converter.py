import http
from typing import Sequence

from lib.converter import Converter
from lib.parser import Parser


class HttpConverter(Converter):
    NAME: str = "http"
    NUMBER_RANGE: Sequence[int] = range(100, 600)

    @staticmethod
    def number2code(number: int) -> str:
        return http.HTTPStatus(int(number)).phrase

    @staticmethod
    def code2number(code: str) -> int:
        return getattr(http.HTTPStatus, code).value

    @staticmethod
    def get_candidates() -> list[str]:
        return dir(http.HTTPStatus)

    @staticmethod
    def number2description(number: int) -> str:
        return http.HTTPStatus(int(number)).description


def main() -> None:
    return Parser.parse(HttpConverter)
