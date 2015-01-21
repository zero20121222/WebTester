# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

import yaml

from basic_db import DBConfig

def __parse_config():
    with open("config/redis.yaml") as r:
        redis = yaml.load(r)
    with open("config/database.yaml") as m:
        mysql = yaml.load(m)
    with open("config/handlers.yaml") as m:
        handlers = yaml.load(m)
    with open("config/env.yaml") as m:
        envSettings = yaml.load(m)
    with open("sql/mapping.yaml") as m:
        mappings = yaml.load(m)
    with open("sql/orm.yaml") as m:
        orm_list = yaml.load(m)
    return redis, mysql, handlers, envSettings, mappings, orm_list

redis_cfg, mysql_cfg, handlers, envSettings, mappings, orm_list = __parse_config()

import redis

def con_redis(env='local'):
    cfg = redis_cfg.get(env)
    pool = redis.ConnectionPool(**cfg)
    return redis.Redis(connection_pool=pool)

def con_mysql(env='local'):
    cfg = dict(mysql_cfg.get(env))
    DBConfig(cfg)

def con_handlers():
    return dict(handlers)

def con_env_settings(env='local'):
    return dict(envSettings.get(env).get("appSettings"))

def con_mappings():
    return dict(mappings)

def con_orm_list():
    return dict(orm_list)
