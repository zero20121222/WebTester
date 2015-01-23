# coding=utf-8
# Date=1/20/15

__author__ = 'MichaelZhao'


import sys
import json
import threading
from time import sleep
from splinter.browser import Browser
from app.lib.helper import Objects
from summary.modules.el_enum import EL_TYPE, ACTION_TYPE

reload(sys)
sys.setdefaultencoding("utf-8")

class TestEngine(object):
    __sleep_time = None

    def __init__(self, browser_name):
        self.browser = Browser(browser_name)

    @staticmethod
    def set_config(config):
        TestEngine.__sleep_time = Objects.first_not_null(config.get("sleep_time"), 2)

    def test_list_acts(self, domain, action_list):
        thread_deal = threading.Thread(target=self.__test_list, args=(domain, action_list), name="TestEngine deal tester")
        thread_deal.start()

    def test_deal(self, domain, action_obj):
        thread_deal = threading.Thread(target=self.__test_do, args=(domain, action_obj), name="TestEngine deal tester")
        thread_deal.start()

    def __test_do(self, domain, action_obj):
        test_url = domain+action_obj.urlPath
        self.browser.visit(test_url)

        if action_obj.forms is not None:
            for form in json.loads(action_obj.forms):
                for el_key, el_val in form["params"].items():
                    self.browser.fill(el_key, el_val.decode("utf-8"))
                    sleep(TestEngine.__sleep_time)

                self.__deal_action(action_obj)
        else:
            self.__deal_action(action_obj)



    def __test_list(self, domain, action_list):
        for action in action_list:
            self.__test_do(domain, action)

    def __event_element(self, el_type, el_value):
        ele_type = EL_TYPE.value(el_type)

        if ele_type == "id":
            return self.browser.find_by_id(el_value)
        elif ele_type == "name":
            return self.browser.find_by_name(el_value)
        elif ele_type == "tag":
            return self.browser.find_by_tag(el_value)
        elif ele_type == "value":
            return self.browser.find_by_value(el_value)
        elif ele_type == "selector":
            return self.browser.find_by_xpath(el_value)
        elif ele_type == "css":
            return self.browser.find_by_css(el_value)
        else:
            raise ValueError("Test Engine can't deal the element type:%s, el_type:%s", ele_type, el_type)

    def __deal_action(self, action_obj):
        action_type = ACTION_TYPE.value(action_obj.action)

        if action_type == "click":
            self.__event_element(action_obj.elType, action_obj.elValue).first.click()
        elif action_type == "double click":
            self.__event_element(action_obj.elType, action_obj.elValue).first.double_click()
        elif action_type == "right click":
            self.__event_element(action_obj.elType, action_obj.elValue).first.right_click()
        elif action_type == "mouse over":
            self.__event_element(action_obj.elType, action_obj.elValue).first.mouse_over()
        elif action_type == "mouse out":
            self.__event_element(action_obj.elType, action_obj.elValue).first.mouse_out()
        elif action_type == "select":
            self.__event_element(action_obj.elType, action_obj.elValue).first.select()
        else:
            print "don't find action for actionId:%s", action_obj.actionId
        sleep(TestEngine.__sleep_time)