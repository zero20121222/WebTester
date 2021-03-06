#! /usr/bin/env python
# -*- encoding: utf8 -*-

__author__ = 'MichaelZhao'

from app.lib.basic_handler import BasicHandler
from summary.daos.action_dao import ActionDao
from summary.modules.test_action import TestAction
from app.lib.helper import JsonHelper
from engine.test_module import TesterData

class ActionHandler(BasicHandler):
    def get(self):
        pass

    def post(self):
        test_action = TestAction(self.request.body)
        test_num = 1
        action_dao = ActionDao()

        action_list = TestAction().to_orm(action_dao.query_max_num(test_action.queueId))
        if len(action_list) != 0:
            test_num = int(action_list[0]["testNum"]) + 1

        action_id = action_dao.create(test_action.queueId, test_num, test_action.urlPath, JsonHelper.dumps(test_action.forms),
                                      JsonHelper.dumps(test_action.actionList), test_action.sleepTime, test_action.waitClose)

        print action_id

class OutActionHandler(BasicHandler):
    def post(self):
        tester_body = JsonHelper.loads(self.request.body)

        tester_data = TesterData(tester_body["domain"], tester_body["testerAction"])

        for action_data in tester_data.testerAction:
            test_action = TestAction(action_data)

            test_num = 1
            action_dao = ActionDao()

            action_list = TestAction().to_orm(action_dao.query_max_num(test_action.queueId))
            if len(action_list) != 0:
                test_num = int(action_list[0]["testNum"]) + 1

            action_id = action_dao.create(test_action.queueId, test_num, test_action.urlPath, JsonHelper.dumps(test_action.forms),
                                          JsonHelper.dumps(test_action.actionList), test_action.sleepTime, test_action.waitClose)