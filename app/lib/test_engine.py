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
    __mouse_over = None
    __mouse_over_sleep = None

    def __init__(self, browser_name):
        self.browser = Browser(browser_name)

    @staticmethod
    def set_config(config):
        TestEngine.__sleep_time = Objects.first_not_null(config.get("sleep_time"), 2)
        TestEngine.__mouse_over = Objects.first_not_null(config.get("mouse_over"), True)
        TestEngine.__mouse_over_sleep = Objects.first_not_null(config.get("mouse_over_sleep"), 1)

    def test_list_acts(self, domain, action_list):
        thread_deal = threading.Thread(target=self.__test_list, args=(domain, action_list), name="TestEngine deal tester")
        thread_deal.start()

    def test_deal(self, domain, action_obj):
        thread_deal = threading.Thread(target=self.__test_do, args=(domain, action_obj), name="TestEngine deal tester")
        thread_deal.start()

    def __test_do(self, domain, action_obj):
        test_url = domain+action_obj.urlPath
        self.browser.visit(test_url)

        # form表单默认为第一个action循环测试，之后的action按照顺序执行
        action_list = json.loads(action_obj.actionList)
        if action_obj.forms is not None:
            form_action = action_list[0]
            for form in json.loads(action_obj.forms):
                for param in form["params"]:
                    self.__set_value(int(param["formType"]), param["formElName"], param["formElValue"].decode("utf-8"))
                    sleep(TestEngine.__sleep_time)

                self.__deal_action(form_action["action"], form_action["elType"], form_action["elValue"])

            for action_deal in action_list[1:]:
                self.__deal_action(action_deal["action"], action_deal["elType"], action_deal["elValue"])
        else:
            for action_deal in action_list:
                self.__deal_action(action_deal["action"], action_deal["elType"], action_deal["elValue"])



    def __test_list(self, domain, action_list):
        for action in action_list:
            self.__test_do(domain, action)


    def __set_value(self, form_type, el_name, el_value):
        if form_type == 1:
            self.browser.fill(el_name, el_value)
        elif form_type == 2:
            self.browser.choose(el_name, el_value)
        elif form_type == 3:
            self.browser.select(el_name, el_value)
        elif form_type == 4:
            self.browser.attach_file(el_name, el_value)
        elif form_type == 5:
            if el_value:
                self.browser.check(el_name)
            else:
                self.browser.uncheck(el_name)
        else:
            raise ValueError("Can't find form type with %s", form_type)


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


    def __deal_action(self, action, el_type, el_value):
        action_type = ACTION_TYPE.value(action)

        # 当页面跳转是抓取最后一个打开的窗口页面
        self.browser.windows.current = self.browser.windows[-1]

        if action_type == "click":
            self.__mouse_of_click(self.__event_element(el_type, el_value).first)
        elif action_type == "double click":
            self.__mouse_of_double_click(self.__event_element(el_type, el_value).first)
        elif action_type == "right click":
            self.__mouse_of_right_click(self.__event_element(el_type, el_value).first)
        elif action_type == "mouse over":
            self.__event_element(el_type, el_value).first.mouse_over()
        elif action_type == "mouse out":
            self.__event_element(el_type, el_value).first.mouse_out()
        elif action_type == "select":
            self.__event_element(el_type, el_value).first.select()
        else:
            print "don't find action for action:%s", action

        sleep(4)


    def __mouse_of_click(self, event_deal_obj):
        if TestEngine.__mouse_over:
            event_deal_obj.mouse_over()
            sleep(TestEngine.__mouse_over_sleep)
            event_deal_obj.click()
        else:
            event_deal_obj.click()


    def __mouse_of_right_click(self, event_deal_obj):
        if TestEngine.__mouse_over:
            event_deal_obj.mouse_over()
            sleep(TestEngine.__mouse_over_sleep)
            event_deal_obj.right_click()
        else:
            event_deal_obj.click()


    def __mouse_of_double_click(self, event_deal_obj):
        if TestEngine.__mouse_over:
            event_deal_obj.mouse_over()
            sleep(TestEngine.__mouse_over_sleep)
            event_deal_obj.double_click()
        else:
            event_deal_obj.click()