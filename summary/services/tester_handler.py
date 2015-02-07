#! /usr/bin/env python
# -*- encoding: utf8 -*-
__author__ = 'MichaelZhao'

from engine.test_engine import TestEngine
from app.lib.basic_handler import BasicHandler
from summary.daos.domain_dao import DomainDao
from summary.daos.action_dao import ActionDao
from summary.modules.test_action import TestAction
from summary.modules.test_domain import TestDomain

class TesterHandler(BasicHandler):
    def get(self):
        domain_id = self.get_argument("domainId")
        queue_id = self.get_argument("queueId")
        action_id_list = self.get_argument("actionIds").split(",")

        domain_obj = TestDomain().to_orm(DomainDao().query_by_id(domain_id), dict_v=False)
        action_list = TestAction().to_orm(ActionDao().query_by_nums(queue_id, test_num=action_id_list), dict_v=False)

        domain = domain_obj[0].domain
        test_engine = TestEngine("chrome")

        test_engine.test_list_acts(domain, action_list)