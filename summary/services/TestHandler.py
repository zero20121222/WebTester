#! /usr/bin/env python
# -*- encoding: utf8 -*-
from summary.modules.test_action import TestAction
from summary.modules.test_domain import TestDomain
from summary.modules.test_queue import TestQueue

__author__ = 'MichaelZhao'

from tornado.web import RequestHandler
from summary.testEngine import TestEngine

class HomeHandler(RequestHandler):
    def get(self):
        forms=[{"testName":"测试未输入用户名",
                "params": {
                    "loginBy":"",
                    "password":"",
                }},
                {"testName":"测试未输入密码",
                "params": {
                    "loginBy":"michael",
                    "password":"",
                }},
                {"testName":"测试帐户不存在",
                "params": {
                    "loginBy":"这是一个不存在的名字",
                    "password":"XXXXXXX",
                }},
                {"testName":"测试成功登录",
                "params": {
                    "loginBy":"v@terminus.io",
                    "password":"123456",
                }}]

        domain_val = {"id":1, "domain":"www.daqihui.cn", "createdAt":"2014-10-10", "updatedAt":"2014-11-10"}
        queue_val = {"id":1, "queueName":"测试登入", "createdAt":"2014-10-10", "updatedAt":"2014-11-10"}
        action_val = {"id":1, "queueId":1, "testNum":1, "urlPath":"www.daqihui.cn", "forms":forms,
                  "actionId":"login-submit", "action":"click", "createdAt":"2014-10-10", "updatedAt":"2014-11-10"}
        self.render("home.html", domain_val=TestDomain(domain_val), queue_val=TestQueue(queue_val), action_val=TestAction(action_val))

class TestHandler(RequestHandler):
    def get(self):
        self.render("edit_view.html", domain="www.daqihui.com")

class EngineHandler(RequestHandler):
    def get(self, *args, **kwargs):
        TestEngine().test()

class EditTesterHandler(RequestHandler):
    def get(self, *args, **kwargs):
        forms=[{"testName":"测试未输入用户名",
                "params": {
                    "loginBy":"",
                    "password":"",
                }},
                {"testName":"测试未输入密码",
                "params": {
                    "loginBy":"michael",
                    "password":"",
                }},
                {"testName":"测试帐户不存在",
                "params": {
                    "loginBy":"这是一个不存在的名字",
                    "password":"XXXXXXX",
                }},
                {"testName":"测试成功登录",
                "params": {
                    "loginBy":"v@terminus.io",
                    "password":"123456",
                }}]

        action_form=[]

        domain_val = {"id":1, "domain":"www.daqihui.cn", "createdAt":"2014-10-10", "updatedAt":"2014-11-10"}
        queue_val = {"id":1, "queueName":"测试登入", "createdAt":"2014-10-10", "updatedAt":"2014-11-10"}
        action_val = {"id":1, "queueId":1, "testNum":1, "urlPath":"www.daqihui.cn", "forms":forms,
                  "actionId":"login-submit", "action":"click", "createdAt":"2014-10-10", "updatedAt":"2014-11-10"}
        self.render("edit_tester.html", domain_val=TestDomain(domain_val), queue_val=TestQueue(queue_val), action_val=TestAction(action_val))
