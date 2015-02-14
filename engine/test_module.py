# coding=utf-8
# Date=1/17/15
import json

__author__ = 'MichaelZhao'

class BasicModule(object):
    def __init__(self, dict_obj=None, deep_split=False):
        if dict_obj is not None:
            dict_values = dict_obj if isinstance(dict_obj, dict) else json.loads(dict_obj)

            for a, b in dict_values.items():
                if deep_split:
                    if isinstance(b, (list, tuple)):
                       setattr(self, a, [BasicModule(x) if isinstance(x, dict) else x for x in b])
                    else:
                       setattr(self, a, BasicModule(b) if isinstance(b, dict) else b)
                else:
                    setattr(self, a, b)

    def dict_to_list(self, dict_list=None):
        obj_queue = []
        if dict_list is not None:
            dict_values = dict_list if isinstance(dict_list, (list, tuple)) else json.loads(dict_list)

            for dict_value in dict_values:
                obj = self.__class__(dict_value)
                obj_queue.append(obj)

        return obj_queue

class TesterData(object):
    '''
    整体测试对象
    '''
    def __init__(self, domain, tester_action):
        self.domain = domain
        self.testerAction = tester_action

class TesterAction(BasicModule):
    '''
    测试处理对象
    '''
    def __init__(self, dict_list=None, deep_split=False):
        self.urlPath = None
        self.forms = None
        self.actionList = None
        self.sleepTime = None
        self.waitClose = None
        BasicModule.__init__(self, dict_list, deep_split)

class TesterForms(BasicModule):
    '''
    表单数据对象
    '''
    def __init__(self, dict_list=None, deep_split=False):
        self.testName = None
        self.params = None
        BasicModule.__init__(self, dict_list, deep_split)

class TesterFormData(BasicModule):
    '''
    具体表单数据
    '''
    def __init__(self, dict_list=None, deep_split=False):
        self.formType = None
        self.formElName = None
        self.formElValue = None
        BasicModule.__init__(self, dict_list, deep_split)

class TesterActionData(BasicModule):
    '''
    测试动作数据
    '''
    def __init__(self, dict_list=None, deep_split=False):
        self.action = None
        self.elType = None
        self.elValue = None
        self.testerResult = None
        BasicModule.__init__(self, dict_list, deep_split)