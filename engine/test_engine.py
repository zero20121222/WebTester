# coding=utf-8
# Date=1/20/15

__author__ = 'MichaelZhao'


import sys
import json
import threading
from time import sleep
from splinter.browser import Browser
from engine.el_enum import EL_TYPE, ACTION_TYPE

reload(sys)
sys.setdefaultencoding("utf-8")

class TestEngine(object):
    __sleep_time = 2
    __mouse_over = True
    __mouse_over_sleep = 1

    def __init__(self, browser_name, execute_path=None):
        if execute_path is None:
            self.__browser = Browser(browser_name)
            self.__quit = False
        else:
            self.__browser = Browser(browser_name, executable_path=execute_path)
            self.__quit = False

    @staticmethod
    def set_config(config):
        TestEngine.__sleep_time = 2 if config.get("sleep_time") is None else config.get("sleep_time")
        TestEngine.__mouse_over = True if config.get("mouse_over") is None else config.get("mouse_over")
        TestEngine.__mouse_over_sleep = 1 if config.get("mouse_over_sleep") is None else config.get("mouse_over_sleep")

    def test_list_acts(self, domain, action_list, back_fun=None, result_back=None):
        thread_deal = threading.Thread(target=self.__test_list_thread, args=(domain, action_list, back_fun, result_back), name="TestEngine deal tester")
        thread_deal.start()

    def test_deal(self, domain, action_obj, back_fun=None, result_back=None):
        thread_deal = threading.Thread(target=self.__test_do_thread, args=(domain, action_obj, back_fun, result_back), name="TestEngine deal tester")
        # hasattr(result_back, "__call__")
        thread_deal.start()

    def quit(self):
        self.__quit = True
        self.__browser.quit()

    def is_quited(self):
        return self.__quit

    def __test_list_thread(self, domain, action_list, back_fun=None, result_back=None):
        try:
            for action in action_list:
                self.__test_do(domain, action)
        except Exception as e:
            raise Exception("[Error code] deal test list failed, error code=", e)
        finally:
            if action_list[0].waitClose != 0:
                sleep(action_list[0].waitClose)

                if back_fun is None:
                    self.quit()
                else:
                    back_fun()


    def __test_do_thread(self, domain, action_obj, back_fun=None, result_back=None):
        try:
            self.__test_do(domain, action_obj)
        except Exception as e:
            raise Exception("[Error code] deal test failed, error code=", e)
        finally:
            if action_obj.waitClose != 0:
                sleep(action_obj.waitClose)

                if back_fun is None:
                    self.quit()
                else:
                    back_fun()


    def __test_do(self, domain, action_obj):
        test_url = domain+action_obj.urlPath
        self.__browser.visit(test_url)

        # form表单默认为第一个action循环测试，之后的action按照顺序执行
        action_list = json.loads(action_obj.actionList) if isinstance(action_obj.actionList, (str, unicode)) else action_obj.actionList
        if action_obj.forms is not None:
            form_action = action_list[0]
            forms = json.loads(action_obj.forms) if isinstance(action_obj.forms, (str, unicode)) else action_obj.forms
            for form in forms:
                for param in form["params"]:
                    self.__set_value(int(param["formType"]), param["formElName"], param["formElValue"].decode("utf-8"))
                    sleep(TestEngine.__sleep_time)

                self.__deal_action(form_action["action"], form_action["elType"], form_action["elValue"])
                sleep(action_obj.sleepTime)

            for action_deal in action_list[1:]:
                self.__deal_action(action_deal["action"], action_deal["elType"], action_deal["elValue"])
                sleep(action_obj.sleepTime)
        else:
            for action_deal in action_list:
                self.__deal_action(action_deal["action"], action_deal["elType"], action_deal["elValue"])
                sleep(action_obj.sleepTime)


    def __set_value(self, form_type, el_name, el_value):
        elements = self.__event_element(form_type, el_name)
        element = elements.first
        if element['type'] in ['text', 'password', 'tel'] or element.tag_name == 'textarea':
            element.value = el_value
        elif element['type'] == 'checkbox':
            if el_value:
                element.check()
            else:
                element.uncheck()
        elif element['type'] == 'radio':
            for field in elements:
                if field.value == el_value:
                    field.click()
        elif element._element.tag_name == 'select':
            element.find_by_value(el_value).first._element.click()
        else:
            element.value = el_value


    def __event_element(self, el_type, el_value):
        ele_type = EL_TYPE.value(el_type)

        if ele_type == "id":
            return self.__browser.find_by_id(el_value)
        elif ele_type == "name":
            return self.__browser.find_by_name(el_value)
        elif ele_type == "tag":
            return self.__browser.find_by_tag(el_value)
        elif ele_type == "value":
            return self.__browser.find_by_value(el_value)
        elif ele_type == "selector":
            return self.__browser.find_by_xpath(el_value)
        elif ele_type == "css":
            return self.__browser.find_by_css(el_value)
        else:
            raise ValueError("Test Engine can't deal the element type:%s, el_type:%s", ele_type, el_type)


    def __deal_action(self, action, el_type, el_value):
        action_type = ACTION_TYPE.value(action)

        # 当页面跳转是抓取最后一个打开的窗口页面
        self.__browser.windows.current = self.__browser.windows[-1]

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
            raise Exception("don't find action for action:%s", action)


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