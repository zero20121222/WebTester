#! /usr/bin/env python
# -*- encoding: utf8 -*-

__author__ = 'MichaelZhao'


class Strings():
    @staticmethod
    def camel_case(s):
        return s[0:1].lower() + s[1:]

    @staticmethod
    def if_empty_null(s):
        if s is None or s == "":
            return True

class Enum(object):
    def __init__(self, dict_val):
        self.__enum = dict_val

    def value(self, index):
        return self.__enum.get(str(index))
