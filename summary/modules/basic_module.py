# coding=utf-8
# Date=1/18/15
import json

__author__ = 'MichaelZhao'

class BasicModule(object):
    def __init__(self, dict_list=None, deep_split=False):
        '''
        根据dict对象或json数据构建对象
        :param dict_list:   dict对象，json数据
        :param deep_split:  是否深度解析数据(递归生成数据对象)
        :return: Obj
        '''
        if dict_list is not None:
            dict_values = dict_list if isinstance(dict_list, dict) else json.loads(dict_list)

            for a, b in dict_values.items():
                if deep_split and isinstance(b, (list, tuple)):
                   setattr(self, a, [BasicModule(x) if isinstance(x, dict) else x for x in b])
                else:
                   setattr(self, a, BasicModule(b) if isinstance(b, dict) else b)

    def to_orm(self, obj_list, dict_v=True):
        '''
        将数据库对应的数据映射到obj对象上
        :param obj_list:    数据库对象
        :param dict_v:      默认转换成映射后的dict，False：obj对象
        :return:dict | obj | [obj]
        '''
        modules = []
        if isinstance(obj_list, (list, tuple)):
            for obj in obj_list:
                module = self.__class__()
                for key, val in obj.items():
                    setattr(module, self.orm_mapping[key], val)

                modules.append(module.__dict__ if dict_v else module)
        else:
            module = self.__class__()
            for key, val in obj_list.items():
                setattr(module, self.orm_mapping[key], val)

            modules.append(module.__dict__ if dict_v else module)

        return modules

    def dict_to_list(self, dict_list=None):
        obj_queue = []
        if dict_list is not None:
            dict_values = dict_list if isinstance(dict_list, (list, tuple)) else json.loads(dict_list)

            for dict_value in dict_values:
                obj = self.__class__(dict_value)
                obj_queue.append(obj)

        return obj_queue