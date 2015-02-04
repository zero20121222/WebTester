# ecoding:utf-8
# testerEnging处理
import json

import struct
import sys
import threading
import Queue
from time import sleep

from splinter import Browser

try:
    import Tkinter
    import tkMessageBox
except ImportError:
    Tkinter = None

# On Windows, the default I/O mode is O_TEXT. Set this to O_BINARY
# to avoid unwanted modifications of the input/output streams.
if sys.platform == "win32":
    import os, msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

# send message to webApp
def send_message(message):
    # 获取信息长度数据
    sys.stdout.write(struct.pack('I', len(message)))

    #写数据
    sys.stdout.write(message)
    sys.stdout.flush()

def read_message_thread(queue):
    while True:
        # 获取webApp传输过来的数据长度(first 4 bytes)
        web_message_length = sys.stdin.read(4)

        if len(web_message_length) == 0:
            if queue:
                queue.put(None)
            sys.exit(0)

        # 获取信息长度
        message_length = struct.unpack('i', web_message_length)[0]

        # 获取json数据
        text = sys.stdin.read(message_length).decode('utf-8')

        if queue:
            queue.put(text)
        else:
            send_message('{"echo": %s}' % text)


# 系统消息信息类型
class MessageInfo(object):
    def __init__(self, m_type, message):
        self.m_type = m_type
        self.message = message

    def __str__(self):
        return json.dumps(self.__dict__)

class MessageDeal(object):
    @staticmethod
    def engine_error(error):
        send_message(MessageInfo("error", error).__str__())

    @staticmethod
    def engine_info(info):
        send_message(MessageInfo("info", info).__str__())

    @staticmethod
    def test_log(info):
        send_message(MessageInfo("log", info).__str__())

    @staticmethod
    def test_result(info):
        send_message(MessageInfo("tResult", info).__str__())

class EngineDealObj(object):
    def __init__(self, method=None, driver=None, execute_path=None, data_obj=None):
        self.method = method
        self.driver = driver
        self.execute_path = execute_path
        self.data_obj = data_obj

    @staticmethod
    def str_to_obj(str_val):
        deal_obj = EngineDealObj()
        try:
            val_dict = json.loads(str_val)
            deal_obj.method = val_dict["method"]
            deal_obj.driver = val_dict["driver"]
            deal_obj.execute_path = val_dict["execute_path"]
            deal_obj.data_obj = val_dict["data_obj"]
            return deal_obj
        except ValueError as e:
            raise ValueError("[Error]EngineDealObj analytical failed, (%s) error code(%s)" % (str_val, e))



class ClientEngine(object):
    __browser = None
    def __init__(self, queue):
        self.queue = queue

    def deal_tester_engine(self):
        while True:
            if not self.queue.empty():
                message = self.queue.get_nowait()

                if message is None:
                    self.__browser.quit()
                    return
                else:
                    self.deal_method(message)
            else:
                sleep(0.1)

    def deal_method(self, message):
        try:
            message_obj = EngineDealObj.str_to_obj(message)
            if message_obj.method == "initEngine":
                ClientEngine.init_Engine(message_obj.driver, message_obj.execute_path)
                MessageDeal.engine_info("[Info]Init clientEngine.")

            elif message_obj.method == "testDeal":
                test_thread = threading.Thread(target=self.test_deal, args=("http://www.daqihui.com/login",))
                test_thread.start()
                MessageDeal.engine_info("[Info]Deal function.")

            else:
                MessageDeal.engine_error("[Error]Can't deal the method %s" % message_obj.method)
        except ValueError as e:
            MessageDeal.engine_error("[Error] value error %s" % e)
        except Exception as e:
            MessageDeal.engine_error("[Error]ClientEngine:deal_method error %s" % e)

    def test_deal(self, url):
        try:
            self.__browser.visit(url)
            testLogin(self.__browser, '测试未输入用户名','','','请输入会员名')
            testLogin(self.__browser, '测试未输入密码','qd_test_001','','请输入密码')
            testLogin(self.__browser, '测试帐户不存在','这是一个不存在的名字哦','xxxxxxx','该账户名不存在')
            testLogin(self.__browser, '测试成功登录','v@terminus.io','123456','企业互惠')

            self.__browser.find_by_css("list-right").first.click()
        except Exception as e:
            MessageDeal.engine_error("[Error]ClientEngine:test_deal error %s" % e)

    @staticmethod
    def init_Engine(driver, executable_path):
        ClientEngine.__browser = Browser(driver, executable_path=executable_path)

def testLogin(browser, desc, userName, passwd, result):
    browser.fill("loginBy", userName.decode("utf-8"))
    browser.fill("password", passwd.decode("utf-8"))
    browser.find_by_id("login-submit").first.click()
    MessageDeal.engine_info("is_text_present:%s" % browser.is_text_present(result))


def Main():
    send_message("Init Tester Engine!")
    queue = Queue.Queue()

    tester = ClientEngine(queue)

    thread = threading.Thread(target=read_message_thread, args=(queue,))
    thread.daemon = True
    thread.start()

    tester.deal_tester_engine()

if __name__ == '__main__':
    Main()