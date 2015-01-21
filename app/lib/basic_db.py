# coding=utf-8
# Date=1/13/15

__author__ = 'MichaelZhao'

from db_engine import DBEngine
from db_engine import TransactionManager


class DBConfig(object):
    __config = None

    def __init__(self, params):
        DBConfig.__config = dict(db="mysql", host=params.get("host"), port=params.get("port"), user=params.get("user"),
                                 passwd=params.get("password"),
                                 dateBase=params.get("database"), minCached=params.get("minCached"), poolOpen=True,
                                 maxShared=params.get("maxShared"),
                                 maxConnections=params.get("maxConnections"), blocking=params.get("blocking"))

    @staticmethod
    def dbConfig():
        return DBConfig.__config


class BasicDB(object):
    @property
    def db(self):
        return DBEngine(**DBConfig.dbConfig())


class BasicTransactional(object):
    @property
    def transactional(self):
        return TransactionManager(**DBConfig.dbConfig())
