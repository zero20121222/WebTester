# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

from app.mapping import sql_mapping


class QueueDao(object):
    def __init__(self):
        pass

    @sql_mapping(sql="insert into test_queues(queue_name, created_at, updated_at) values(%s,now(),now())", method="create")
    def create(self, queue_name):
        if not isinstance(queue_name, str):
            raise ValueError("create failed error code domain str, queue_name:%s", queue_name)

    @sql_mapping(sql="select * from test_queues where id=%s", method="query")
    def query_by_id(self, id):
        if not isinstance(id, int):
            raise ValueError("query failed error code id Integer, id:%s", id)

    @sql_mapping(sql="select * from test_queues where queue_name=%s", method="query")
    def query_by_name(self, queue_name):
        if not isinstance(queue_name, str):
            raise ValueError("query failed error code queue_name Str, queue_name:%s", queue_name)

    @sql_mapping(sql="select * from test_queues", method="query")
    def query_all(self):
        pass