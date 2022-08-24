#!/usr/bin/env python3
# coding=utf-8

from enum import Enum
import logging
import os
import re
import subprocess
import sys


logger = logging.getLogger(__name__)


class Converter(object):
    NAME = None
    NUMBER_RANGE = ()

    @staticmethod
    def number2code(number):
        raise NotImplementedError

    @staticmethod
    def code2number(code):
        raise NotImplementedError

    @staticmethod
    def number2description(number):
        raise NotImplementedError

    @staticmethod
    def get_candidates():
        raise NotImplementedError

    @classmethod
    def print_version(cls):
        """
        Print Git project version by running ``git describe --tags`` in this project.
        """

        project_dir = os.path.dirname(__file__)
        with open(os.devnull, 'wb') as devnull:
            version = subprocess.check_output(['git', 'describe', '--tags'], stderr=devnull, cwd=project_dir)
            version = version.rstrip()
        if hasattr(version, 'decode'):
            version = version.decode('utf-8')
        print(f"{sys.argv[0]} version {version}")

    @classmethod
    def print_help(cls):
        print("{cmd} [-v] list|<{name}-number>|<{name}-name>".format(cmd=sys.argv[0], name=cls.NAME))

    @classmethod
    def convert(cls, number=None, code=None, verbose=False):
        """
        :param int number: 
        :param str code: 
        :param bool verbose:
        :rtype: str
        """
        n = cls.code2number(code) if number is None else number
        c = cls.number2code(number) if code is None else code

        if verbose:
            return "{n:3d} - {c:15}: {d}".format(n=n, c=c, d=cls.number2description(n))
        else:
            if code is None:
                return c
            elif number is None:
                return str(n)
            else:
                return "{n:3d} - {c}".format(n=n, c=c)

    @classmethod
    def parse(cls):

        if len(sys.argv) < 2:
            cls.print_help()
            exit()

        invalids = dict()
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
                    print(cls.convert(number=n, code=cls.number2code(n), verbose=bool(verbose_option)))
                except Exception as e:
                    invalids[n] = e

        elif code_or_number.isdigit():
            try:
                print(cls.convert(number=int(code_or_number), verbose=bool(verbose_option)))
            except Exception as e:
                invalids[code_or_number] = e

        else:
            try:
                print(cls.convert(code=code_or_number, verbose=bool(verbose_option)))
            except Exception as e:
                if verbose_option:
                    print(
                        "No {name} matched the input {i!r} ({e}). Try to match as re:".format(
                             name=cls.NAME,          i=code_or_number, e=e),
                        file=sys.stderr,
                    )
                search = re.compile(code_or_number, flags=re.IGNORECASE)
                for att in cls.get_candidates():
                    try:
                        number = cls.code2number(att)
                        desc = cls.number2description(number)
                        if search.search(att) or search.search(str(number)) or search.search(desc) and bool(verbose_option):
                            print(cls.convert(number=number, code=att, verbose=bool(verbose_option)))
                    except:
                        pass

        if invalids and verbose_option:
            if all(isinstance(e, (ValueError, KeyError)) for e in invalids.values()):
                print("invalids: {}".format(set(invalids.keys())), file=sys.stderr)
            else:
                print("invalids: {}".format(invalids), file=sys.stderr)
