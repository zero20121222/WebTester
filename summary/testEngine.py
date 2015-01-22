# coding=utf-8
# Date=1/14/15
from time import sleep

__author__ = 'MichaelZhao'

# coding=utf-8
# 实现python的测试管理工具类

import sys
from splinter.browser import Browser

reload(sys)
sys.setdefaultencoding("utf-8")

output = lambda desc: desc.encode("utf-8")


class TestEngine(object):
    __testUrl = "http://www.daqihui.cn/login"
    __browser = None

    def test(self):
        TestEngine.__browser = TestEngine.__browser if TestEngine.__browser is not None else Browser("chrome")
        TestEngine.__browser.visit(TestEngine.__testUrl)
        output("测试页面:" + TestEngine.__browser.title)

        try:
            '''
            数据库设计：
            id, domain, created_at, updated_at
            id, queue_name, created_at, updated_at
            id, queue_id, test_num, urlPath, forms, action_id, action, created_at, updated_at

            forms=[{
                testName:"",
                loginBy:"",
                password:"",
            },{
                testName:"",
                loginBy:"",
                password:"",
            }]
            '''
            self.testLogin('测试未输入用户名', '', '', '企业互惠')
            self.testLogin('测试未输入密码', 'qd_test_001', '', '请输入密码')
            self.testLogin('测试帐户不存在', '这是一个不存在的名字哦', 'xxxxxxx', '该账户名不存在')
            # 校验登入是否成功
            self.testLogin('测试成功登录', 'v@terminus.io', '123456', '企业互惠')
        except Exception as e:
            print "Error:", e


    def testLogin(slef, desc, userName, passwd, result):
        output(desc)
        TestEngine.__browser.fill("loginBy", userName.decode("utf-8"))
        TestEngine.__browser.fill("password", passwd.decode("utf-8"))
        TestEngine.__browser.find_by_id("login-submit").first.click()
        sleep(2)

TestEngine().test()