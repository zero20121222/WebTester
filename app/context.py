# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

import lib
'''
初始化DB
'''
lib.con_mysql()

'''
初始化tester Engine的（后期会将tester与server端分离）
'''
lib.con_tester_conf()

'''
server端的web域名
'''
domain = lib.con_domain()

'''
redis的配置
'''
redis = lib.con_redis()

'''
handler的映射url路径的关联
'''
handlers = lib.con_handlers()

'''
系统环境的配置管理
'''
envSettings = lib.con_env_settings()

'''
sql的mapping映射关系(可以直接使用sql_mapping装饰器来进行sql处理)
'''
mapping = lib.con_mappings()

'''
数据库字段与对象的关系映射
'''
orm_list = lib.con_orm_list()