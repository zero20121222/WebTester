# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

from app.mapping import sql_mapping

class TestDao(object):
    def __init__(self):
        pass

    @sql_mapping("select * from ecp_users where id=1", method="query")
    def query_one(self):
        pass

    @sql_mapping()
    def query(self, limit):
        pass
