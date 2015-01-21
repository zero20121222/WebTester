# coding=utf-8
# Date=1/21/15

__author__ = 'MichaelZhao'
import json
from tornado.web import RequestHandler

def json_to_dict(str_val):
    return json.loads(str_val)

class BasicHandler(RequestHandler):
    def render(self, template_name, **kwargs):
        params = dict()
        for key, val in self.request.arguments.items():
            params[key] = ','.join(val) if isinstance(val, list) else val

        kwargs["params"] = params
        kwargs["json_dict"] = json_to_dict
        RequestHandler.render(self, template_name, **kwargs)
