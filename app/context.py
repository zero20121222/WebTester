# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

import lib

# todo: read from properties
domain = r'localhost'

redis = lib.con_redis()
db = lib.con_mysql()
handlers = lib.con_handlers()
envSettings = lib.con_env_settings()
mapping = lib.con_mappings()
orm_list = lib.con_orm_list()