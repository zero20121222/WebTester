#! /usr/bin/env python
# -*- encoding: utf8 -*-

__author__ = 'MichaelZhao'

from app.lib.basic_handler import BasicHandler
from summary.daos.queue_dao import QueueDao

class QueueHandler(BasicHandler):
    def get(self):
        pass

    def post(self, *args, **kwargs):
        queue_dao = QueueDao()
        queue_name = self.get_argument("testQueue")

        queue_list = queue_dao.query_by_name(queue_name)
        queue_id = 0
        if len(queue_list) <= 0:
            queue_id = queue_dao.create(queue_name)

        print queue_id