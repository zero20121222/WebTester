# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

from app.mapping import sql_mapping


class DomainDao(object):
    def __init__(self):
        pass

    @sql_mapping(sql="insert into test_domains(domain, created_at, updated_at) values(%s,now(),now())", method="create")
    def create(self, domain):
        if not isinstance(domain, str):
            raise ValueError("create failed error code domain str, domain:%s", domain)

    @sql_mapping(sql="select * from test_domains where id=%s", method="query")
    def query_by_id(self, id):
        if not isinstance(id, int):
            raise ValueError("query failed error code id Integer, id:%s", id)

    @sql_mapping(sql="select * from test_domains where domain=%s", method="query")
    def query_by_name(self, domain_name):
        if not isinstance(domain_name, str):
            raise ValueError("query failed error code domain_name Str, domain_name:%s", domain_name)

    @sql_mapping(sql="select * from test_domains", method="query")
    def query_all(self):
        pass