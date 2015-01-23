# coding=utf-8
# Date=1/17/15
__author__ = 'MichaelZhao'

from summary.modules.basic_module import BasicModule

'''
--
CREATE TABLE `test_actions` (
  `id`                 BIGINT(20)        NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `queue_id`           BIGINT(20)        NULL     COMMENT '队列编号',
  `test_num`           INT               NULL     COMMENT '顺序编号',
  `url`                VARCHAR(128)      NULL     COMMENT '测试url',
  `forms`              VARCHAR(1024)     NULL     COMMENT '表单数据填写',
  `action_list`        VARCHAR(1024)     NULL     COMMENT '连续的测试动作',
  `sleep_time`         SMALLINT          NULL     COMMENT '每个事件的间隔时间',
  `wait_close`         SMALLINT          NULL     COMMENT '测试浏览器自动关闭时间',
  `created_at`         DATETIME          NOT NULL COMMENT '创建时间',
  `updated_at`         DATETIME          NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
);
CREATE INDEX `test_actions_queue_id` ON test_actions(`queue_id`);

forms=[{"testName":"测试未输入用户名",
        "params": [{
            "form_type":"text, radio, select, file, checked",
            "form_el_name":"loginBy",
            "form_el_value":"michael",
        },{
            "form_type":"text, radio, select, file, checked, unchecked",
            "form_el_name":"loginBy",
            "form_el_value":"michael",
        }]}]
action_list=[{
            el_type:id,
            el_value:login_by,
            action:click
        },{
            el_type:id,
            el_value:login_by,
            action:click
        }]
'''
class TestAction(BasicModule):
    def __init__(self, dict_list=None, deep_split=False):
        self.id = None
        self.queueId = None
        self.testNum = None
        self.urlPath = None
        self.forms = None
        self.actionList = None
        self.sleepTime = None
        self.waitClose = None
        self.createdAt = None
        self.updatedAt = None
        BasicModule.__init__(self, dict_list, deep_split)

