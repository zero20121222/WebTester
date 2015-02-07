# coding=utf-8
# Date=1/17/15
import json

__author__ = 'MichaelZhao'

class TesterData(object):
    def __init__(self, domain, tester_action=list):
        self.domain = domain
        self.testerAction = tester_action

class TesterAction(object):
    def __init__(self, url_path=None, forms=None, action_list=None, sleep_time=None, wait_close=None):
        self.urlPath = url_path
        self.forms = forms
        self.actionList = action_list
        self.sleepTime = sleep_time
        self.waitClose = wait_close

    def dict_to_list(self, dict_list=None):
        obj_queue = []
        if dict_list is not None:
            dict_values = dict_list if isinstance(dict_list, (list, tuple)) else json.loads(dict_list)

            for dict_value in dict_values:
                obj = self.__class__(dict_value)
                obj_queue.append(obj)

        return obj_queue