# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

import tornado.ioloop
import tornado.web
import app
import os.path


class BasicApp(tornado.web.Application):
    def __init__(self):
        handlers = []

        paths = os.path.dirname(__file__).split("/")
        static_path = ""
        for path in paths[0:-2]:
            static_path += path+"/"

        if app.context.envSettings.get("template_path") is None:
            app.context.envSettings["template_path"] = os.path.join(static_path, "templates")

        if app.context.envSettings.get("static_path") is None:
            app.context.envSettings["static_path"] = os.path.join(static_path, "statics")

        tornado.web.Application.__init__(self, handlers, **app.context.envSettings)
        app.scan_modules(self, app.context)
