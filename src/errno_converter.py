#!/usr/bin/env python3
# coding=utf-8
import os
import errno
from converter_lib import Converter


class ErrnoConverter(Converter):
    NAME = "errno"
    NUMBER_RANGE = range(1, 132)

    @staticmethod
    def number2code(number):
        return errno.errorcode[int(number)]

    @staticmethod
    def code2number(code):
        return getattr(errno, code)

    @staticmethod
    def get_candidates():
        return dir(errno)

    @staticmethod
    def number2description(number):
        return os.strerror(number)

def main():
    return ErrnoConverter.parse()
