#!/usr/bin/env python3
# coding=utf-8
import signal
from converter_lib import Converter


class SignalConverter(Converter):
    NAME = "signal"
    NUMBER_RANGE = range(1, 65)

    @staticmethod
    def number2code(number):
        return signal.Signals(int(number)).name

    @staticmethod
    def code2number(code):
        return getattr(signal, code).value

    @staticmethod
    def get_candidates():
        return dir(signal)

    @staticmethod
    def number2description(number):
        return signal.strsignal(signal.Signals(int(number)))  # Python3.8

def main():
    return SignalConverter.parse()

