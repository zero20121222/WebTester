# coding=utf-8
# Date=1/14/15

__author__ = 'MichaelZhao'

import yaml
import redis
from basic_db import DBConfig
from engine.test_engine import TestEngine

def __parse_config():
    with open("config/redis.yaml") as m:
        redis = yaml.load(m)

    with open("config/database.yaml") as m:
        mysql = yaml.load(m)

    with open("config/handlers.yaml") as m:
        handlers = yaml.load(m)

    with open("config/env.yaml") as m:
        envSettings = yaml.load(m)

    with open("config/tester_config.yaml") as m:
        tester_config = yaml.load(m)

    with open("sql/mapping.yaml") as m:
        mappings = yaml.load(m)

    with open("sql/orm.yaml") as m:
        orm_list = yaml.load(m)

    return redis, mysql, handlers, envSettings, tester_config, mappings, orm_list

redis_cfg, mysql_cfg, handlers, envSettings, tester_config, mappings, orm_list = __parse_config()


def con_redis(env='local'):
    cfg = redis_cfg.get(env)
    pool = redis.ConnectionPool(**cfg)
    return redis.Redis(connection_pool=pool)

def con_mysql(env='local'):
    cfg = dict(mysql_cfg.get(env))
    DBConfig(cfg)

def con_env_settings(env='local'):
    return dict(envSettings.get(env).get("appSettings"))

def con_tester_conf(env='local'):
    config = dict(tester_config.get(env))
    TestEngine.set_config(config)

def con_domain(env='local'):
    return envSettings.get(env).get("domain")

def con_mappings():
    return dict(mappings)

def con_orm_list():
    return dict(orm_list)

def con_handlers():
    return dict(handlers)
