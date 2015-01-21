# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

import functools
from lib.basic_db import BasicDB
import context

__mapping = context.mapping
def sql_mapping(sql=None, method=None):
    '''
    对于一些特殊操作例如in操作查询的直接需要在传递参数时标明dict对应的index,in的传参直接使用(?)标注
    as :
    @sql_mapping(sql="select * from test_actions where queue_id=%s and test_num in (?)", method="query")
    def query_by_queue_id(self, queue_id, test_num):
        pass
    test_num必须和in的对象相对应,在传递参数的时候需要标明
    调用:
    action_dao.query_by_queue_id(queue_id, test_num=[1, 2])
    :param sql:
    :param method:
    :return:
    '''
    def _sql_mapping(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kw):

            if sql is not None:
                deal_sql = sql
                deal_method = method
            else:
                map_value = __mapping[fun.__module__][args[0].__class__.__name__][fun.__name__]
                deal_sql = map_value["sql"]
                deal_method = map_value["method"]

            if deal_sql is None:
                raise ValueError("[Error] Class:%s Method:%s sql mapping sql can't be None" % (args[0].__class__.__name__, fun.__name__))

            if deal_method is None:
                raise ValueError("[Error] Class:%s Method:%s sql mapping method can't be None" % (args[0].__class__.__name__, fun.__name__))

            args_val = list(args[1:])
            for val in kw.values():
                args_val.extend(val)

            deal_sql = __with_in(deal_sql, kw)

            if deal_method == "query":
                return BasicDB().db.query(deal_sql, args_val)
            elif deal_method == "update":
                return BasicDB().db.update(deal_sql, args_val)
            elif deal_method == "delete":
                return BasicDB().db.delete(deal_sql, args_val)
            elif deal_method == "create":
                return BasicDB().db.create(deal_sql, args_val)
            else:
                raise Exception("[Error] sql deal method:%s undefined, sql method(create, update, delete, query)", deal_method)
        return wrapper
    return _sql_mapping

def __with_in(sql, column_values):
    deal_sql = sql
    columns = __of_with_in(sql)

    if len(columns) > 0:
        for column in columns[::-1]:
            col_num = len(column_values[column])

            insert_val = ""
            for i in range(1, col_num):
                insert_val += "%s,"
            insert_val += "%s"

            deal_sql = deal_sql.replace("?", insert_val, 1)

    return deal_sql

def __of_with_in(sql):
    exist_in = sql.count("in") > 0

    columns = []
    if exist_in:
        in_index = False
        for tar_v in sql.split(" ")[::-1]:
            if in_index:
                columns.append(tar_v)
                in_index = False
            if tar_v == "in":
                in_index = True

    return columns
