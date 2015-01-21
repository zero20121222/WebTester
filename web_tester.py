# coding=utf-8
# Date=1/14/15
from summary.modules.test_action import TestAction

__author__ = 'MichaelZhao'

import tornado.httpserver
import tornado.options
import tornado.ioloop

from app.lib.basic_app import BasicApp

application = BasicApp()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()