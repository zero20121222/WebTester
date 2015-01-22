#! /usr/bin/env python
# -*- encoding: utf8 -*-

__author__ = 'MichaelZhao'

from app.lib.basic_handler import BasicHandler
from summary.daos.domain_dao import DomainDao
from summary.daos.queue_dao import QueueDao
from summary.daos.action_dao import ActionDao
from summary.modules.test_action import TestAction
from summary.modules.test_domain import TestDomain
from summary.modules.test_queue import TestQueue
from summary.modules.el_enum import EL_TYPE, ACTION_TYPE

class HomeHandler(BasicHandler):
    def get(self):
        queue_id = self.get_argument("queueId", None)

        domain_dao = DomainDao()
        domain_list = domain_dao.query_all()
        domain_values = TestDomain().to_orm(domain_list, dict_v=False)

        queue_dao = QueueDao()
        queue_list = queue_dao.query_all()
        queue_values = TestQueue().to_orm(queue_list, dict_v=False)

        action_dao = ActionDao()
        action_list = action_dao.query_by_queue_id(queue_id if queue_id is not None else queue_values[0].id)
        action_values = TestAction().to_orm(action_list, dict_v=False)

        self.render("home.html", domain_values=domain_values, queue_values=queue_values,
                    action_values=action_values, EL_TYPE=EL_TYPE, ACTION_TYPE=ACTION_TYPE)


class EditHandler(BasicHandler):
    def get(self):
        domain_dao = DomainDao()
        domain_list = domain_dao.query_all()
        domain_values = TestDomain().to_orm(domain_list, dict_v=False)

        queue_dao = QueueDao()
        queue_list = queue_dao.query_all()
        queue_values = TestQueue().to_orm(queue_list, dict_v=False)

        action_dao = ActionDao()
        action_list = action_dao.query_by_queue_id(queue_values[0].id)
        action_values = TestAction().to_orm(action_list)

        self.render("edit_tester.html", domain_values=domain_values, queue_values=queue_values, action_values=action_values)

    def post(self, *args, **kwargs):
        pass