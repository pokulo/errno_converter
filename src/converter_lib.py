import abc
import logging
import os
import re
import subprocess
import sys
from typing import Sequence

logger = logging.getLogger(__name__)


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

    @classmethod
    def print_version(cls):
        """Print Git project version by running ``git describe --tags`` in this project."""

        project_dir = os.path.dirname(__file__)
        with open(os.devnull, "wb") as devnull:
            version = subprocess.check_output(
                ["git", "describe", "--tags"], stderr=devnull, cwd=project_dir
            )
            version = version.rstrip()
        if hasattr(version, "decode"):
            version = version.decode("utf-8")
        print(f"{sys.argv[0]} version {version}")

    @classmethod
    def print_help(cls) -> None:
        """Prints help text to cli."""
        print(
            "{cmd} [-v] list|<{name}-number>|<{name}-name>".format(
                cmd=sys.argv[0], name=cls.NAME
            )
        )

    @classmethod
    def _convert(
        cls, number: int | None = None, code: str | None = None, verbose: bool = False
    ) -> str:
        n = cls.code2number(code) if number is None and code is not None else number
        c = cls.number2code(number) if number is not None and code is None else code

        if n is None or c is None:
            raise Exception("Either number or code must be provided.")

        if verbose:
            return f"{n:3d} - {c:15}: {cls.number2description(n)}"

        if code is None:
            return c

        if number is None:
            return str(n)

        return f"{n:3d} - {c}"

    @classmethod
    def parse(cls) -> None:
        """Parse cli arguments, convert code and print result."""

        if len(sys.argv) < 2:
            cls.print_help()
            exit()

        invalids = {}
        verbose_option = sys.argv[1]
        if verbose_option == "-v":
            if len(sys.argv) < 3:
                try:
                    cls.print_version()
                except Exception as exc:
                    logger.error(f"Printing version (git tag) ommited due to: {exc}")
                    cls.print_help()
                exit()
            code_or_number = sys.argv[2]
        else:
            verbose_option = ""
            code_or_number = sys.argv[1]

        if code_or_number.lower() == "list":
            for n in cls.NUMBER_RANGE:
                try:
                    print(
                        cls._convert(
                            number=n,
                            code=cls.number2code(n),
                            verbose=bool(verbose_option),
                        )
                    )
                except Exception as e:
                    invalids[n] = e

        elif code_or_number.isdigit():
            number = int(code_or_number)
            try:
                print(cls._convert(number=number, verbose=bool(verbose_option)))
            except Exception as e:
                invalids[number] = e

        else:
            try:
                print(cls._convert(code=code_or_number, verbose=bool(verbose_option)))
            except Exception as e:
                if verbose_option:
                    print(
                        "No {name} matched the input {i!r} ({e}). Try to match as re:".format(
                            name=cls.NAME, i=code_or_number, e=e
                        ),
                        file=sys.stderr,
                    )
                search = re.compile(code_or_number, flags=re.IGNORECASE)
                for att in cls.get_candidates():
                    try:
                        number = cls.code2number(att)
                        desc = cls.number2description(number)
                        if (
                            search.search(att)
                            or search.search(str(number))
                            or search.search(desc)
                            and bool(verbose_option)
                        ):
                            print(
                                cls._convert(
                                    number=number,
                                    code=att,
                                    verbose=bool(verbose_option),
                                )
                            )
                    except:
                        pass

        if invalids and verbose_option:
            if all(isinstance(e, (ValueError, KeyError)) for e in invalids.values()):
                print(f"invalids: {set(invalids.keys())}", file=sys.stderr)
            else:
                print(f"invalids: {invalids}", file=sys.stderr)
