# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

from app.mapping import sql_mapping


class TestDao(object):
    def __init__(self):
        pass

    # id, queue_id, test_num, urlPath, forms, action_id, action, created_at, updated_at
    @sql_mapping(sql="select * from ecp_users limit %s", method="query")
    def salute(self, limit):
        if not isinstance(limit , int):
            raise ValueError("query failed error code limit must Integer, limit:%s", limit)