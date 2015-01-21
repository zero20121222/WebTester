#! /usr/bin/env python
# -*- encoding: utf8 -*-
__author__ = 'MichaelZhao'

from app.lib.basic_handler import BasicHandler
from summary.daos.domain_dao import DomainDao

class DomainHandler(BasicHandler):
    def get(self):
        pass

    def post(self, *args, **kwargs):
        test_domain = self.get_argument("testDomain")
        domain_dao = DomainDao()

        domain_list = domain_dao.query_by_name(test_domain)
        domain_id = 0
        if len(domain_list) <= 0:
            domain_id = domain_dao.create(test_domain)

        print domain_id