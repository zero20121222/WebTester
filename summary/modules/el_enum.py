# coding=utf-8
# Date=1/22/15
__author__ = 'MichaelZhao'

from app.lib.units import Enum

EL_TYPE = Enum({"1": "id", "2": "name", "3": "tag", "4": "value", "5": "selector", "6": "css"})

ACTION_TYPE = Enum({"1": "click", "2": "double click", "3": "right click", "4": "mouse over", "5": "mouse out", "6": "select"})