import logging
import os
import re
import subprocess
import sys
from importlib.metadata import version as get_version, PackageNotFoundError

from .converter import Converter


logger = logging.getLogger(__name__)


class Parser:
    @staticmethod
    def _print_version():
        """Print Git project version by running ``git describe --tags`` in this project."""

        try:
            version = get_version("errno-converter")
        except PackageNotFoundError:
            project_dir = os.path.dirname(__file__)
            with open(os.devnull, "wb") as devnull:
                version = subprocess.check_output(
                    ["git", "describe", "--tags"], stderr=devnull, cwd=project_dir
                )
                version = version.rstrip()
            if hasattr(version, "decode"):
                version = version.decode("utf-8")
        print(f"{sys.argv[0]} version {version}")

    @staticmethod
    def _print_help(converter: type[Converter]) -> None:
        """Prints help text to cli."""
        print(
            "{cmd} [-v] list|<{name}-number>|<{name}-name>".format(
                cmd=sys.argv[0], name=converter.NAME
            )
        )

    @staticmethod
    def _convert(
        converter: type[Converter],
        number: int | None = None,
        code: str | None = None,
        verbose: bool = False,
    ) -> str:
        n = (
            converter.code2number(code)
            if number is None and code is not None
            else number
        )
        c = (
            converter.number2code(number)
            if number is not None and code is None
            else code
        )

        if n is None or c is None:
            raise Exception("Either number or code must be provided.")

        if verbose:
            return f"{n:3d} - {c:15}: {converter.number2description(n)}"

        if code is None:
            return c

        if number is None:
            return str(n)

        return f"{n:3d} - {c}"

    @classmethod
    def parse(cls, converter: type[Converter]) -> None:
        """Parse cli arguments, convert code and print result."""

        if len(sys.argv) < 2:
            cls._print_help(converter)
            exit()

        invalids = {}
        verbose_option = sys.argv[1]
        if verbose_option == "-v":
            if len(sys.argv) < 3:
                try:
                    cls._print_version()
                except Exception as exc:
                    logger.error(f"Printing version (git tag) ommited due to: {exc}")
                    cls._print_help(converter)
                exit()
            code_or_number = sys.argv[2]
        else:
            verbose_option = ""
            code_or_number = sys.argv[1]

        if code_or_number.lower() == "list":
            for n in converter.NUMBER_RANGE:
                try:
                    print(
                        cls._convert(
                            converter=converter,
                            number=n,
                            code=converter.number2code(n),
                            verbose=bool(verbose_option),
                        )
                    )
                except Exception as e:
                    invalids[n] = e

        elif code_or_number.isdigit():
            number = int(code_or_number)
            try:
                print(
                    cls._convert(
                        converter=converter, number=number, verbose=bool(verbose_option)
                    )
                )
            except Exception as e:
                invalids[number] = e

        else:
            try:
                print(
                    cls._convert(
                        converter=converter,
                        code=code_or_number,
                        verbose=bool(verbose_option),
                    )
                )
            except Exception as e:
                if verbose_option:
                    print(
                        "No {name} matched the input {i!r} ({e}). Try to match as re:".format(
                            name=converter.NAME, i=code_or_number, e=e
                        ),
                        file=sys.stderr,
                    )
                search = re.compile(code_or_number, flags=re.IGNORECASE)
                for att in converter.get_candidates():
                    try:
                        number = converter.code2number(att)
                        desc = converter.number2description(number)
                        if (
                            search.search(att)
                            or search.search(str(number))
                            or search.search(desc)
                            and bool(verbose_option)
                        ):
                            print(
                                cls._convert(
                                    converter=converter,
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
