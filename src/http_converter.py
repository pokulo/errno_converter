#!/usr/bin/env python3
# coding=utf-8
import http

from converter_lib import Converter


class HttpConverter(Converter):
    NAME = "http"
    NUMBER_RANGE = range(100, 600)

    @staticmethod
    def number2code(number):
        return http.HTTPStatus(int(number)).phrase

    @staticmethod
    def code2number(code):
        return getattr(http.HTTPStatus, code).value

    @staticmethod
    def get_candidates():
        return dir(http.HTTPStatus)

    @staticmethod
    def number2description(number):
        return http.HTTPStatus(int(number)).description

def main():
    return HttpConverter.parse()

