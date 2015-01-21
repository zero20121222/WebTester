# coding=utf-8
# Date=1/14/15

__author__ = 'MichaelZhao'

from tornado.web import RequestHandler
from summary.modules.basic_module import BasicModule

def scan_modules(application, context):
    # 装载orm对象关联关系
    for path in context.orm_list.keys():
        class_name, module_name, module_path = __class_path(path)
        cls_module = __import__(module_path, {}, {}, [module_name])
        class_obj = getattr(cls_module, class_name)

        if issubclass(class_obj, BasicModule):
            setattr(class_obj, "orm_mapping", context.orm_list[path]["columns"])
        else:
            raise NotImplementedError("ClassObj:%s must extend BasicModule", class_obj)

    # 装载handler的映射关系
    for path in context.handlers.keys():
        class_name, module_name, module_path = __class_path(path)
        cls_module = __import__(module_path, {}, {}, [module_name])
        class_obj = getattr(cls_module, class_name)

        if issubclass(class_obj, RequestHandler):
            application.add_handlers(context.domain, [
                (context.handlers[path]['url'], class_obj),
            ])

        else:
            raise NotImplementedError("ClassObj:%s must extend RequestHandler", class_obj)


def __class_path(handler_path):
    values = handler_path.split(".")
    class_name, module_name = values[::-1][0:2]

    module_path = ""
    for value in values[0:-2]:
        module_path += value + "."
    module_path += module_name

    return class_name, module_name, module_path
