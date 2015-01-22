# coding=utf-8
# Date=1/21/15
__author__ = 'MichaelZhao'

import json

class JsonHelper(object):
    @staticmethod
    def dumps(dict_val):
        if dict_val is not None:
            return json.dumps(dict_val, ensure_ascii=False)
        else:
            return None

class Objects(object):
    def __init__(self):
        pass

    @staticmethod
    def first_not_null(obj, default_obj):
        if obj is None:
            return default_obj

        return default_obj