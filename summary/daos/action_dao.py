# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

from app.mapping import sql_mapping


class ActionDao(object):
    def __init__(self):
        pass

    @sql_mapping(sql="insert into test_actions(queue_id, test_num, url_path, forms, el_type, el_value, action, created_at, updated_at) values(%s, %s, %s, %s, %s, %s, %s, now(), now())", method="create")
    def create(self, queueId, testNum, urlPath, forms, actionId, action):
        pass

    @sql_mapping(sql="select * from test_actions where id=%s", method="query")
    def query_by_id(self, id):
        if not isinstance(id, int):
            raise ValueError("query failed error code id Integer, id:%s", id)

    @sql_mapping(sql="select * from test_actions where queue_id=%s order by test_num", method="query")
    def query_by_queue_id(self, queue_id):
        pass

    @sql_mapping(sql="select * from test_actions where queue_id=%s order by test_num desc", method="query")
    def query_max_num(self, queue_id):
        pass

    @sql_mapping(sql="select * from test_actions where queue_id=%s and test_num in (?) order by test_num", method="query")
    def query_by_nums(self, queue_id, test_num):
        pass