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
    def __init__(self, domain, tester_action):
        self.domain = domain
        self.testerAction = tester_action

class TesterAction(BasicModule):
    def __init__(self, dict_list=None, deep_split=False):
        self.urlPath = None
        self.forms = None
        self.actionList = None
        self.sleepTime = None
        self.waitClose = None
        BasicModule.__init__(self, dict_list, deep_split)

if __name__ == "__main__":
    obj = TesterData({"domain":"http://www.daqihui.com", "testerAction":[{"urlPath":"/login",
            "forms":[{"params": [{"formType": "1", "formElName": "loginBy", "formElValue": "v@terminus.io"}, {"formType": "1", "formElName": "password", "formElValue": "123456"}], "testName": "测试用户登入"}],
            "actionList":[{"action": "1", "elType": "1", "elValue": "login-submit"}, {"action": "1", "elType": "6", "elValue": ".shop-list"}, {"action": "1", "elType": "6", "elValue": ".btn-danger"}, {"action": "1", "elType": "6", "elValue": ".btn-success"}, {"action": "1", "elType": "6", "elValue": ".btn-medium"}]}]})
    print json.dumps(TesterAction().dict_to_list(obj.testerAction)[0].__dict__)