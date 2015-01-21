# coding=utf-8
# Date=1/17/15
__author__ = 'MichaelZhao'

from summary.modules.basic_module import BasicModule
from app.lib.units import Enum

'''
--
CREATE TABLE `test_actions` (
  `id`                 BIGINT(20)        NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `queue_id`           BIGINT(20)        NULL     COMMENT '队列编号',
  `test_num`           INT               NULL     COMMENT '顺序编号',
  `url_path`           VARCHAR(128)      NULL     COMMENT '测试url',
  `forms`              VARCHAR(512)      NULL     COMMENT '表单数据填写',
  `el_type`            VARCHAR(32)       NULL     COMMENT '元素对象的定位（1.id, 2.name, 3.tag, 4.value, 5.selector, 6.css）',
  `el_value`           VARCHAR(64)       NULL     COMMENT '元素定位名称',
  `action`             VARCHAR(32)       NULL     COMMENT '事件名称（click）',
  `created_at`         DATETIME          NOT NULL COMMENT '创建时间',
  `updated_at`         DATETIME          NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
);
CREATE INDEX `test_actions_queue_id` ON test_actions(`queue_id`);
'''
class TestAction(BasicModule):
    def __init__(self, dict_list=None, deep_split=False):
        self.id = None
        self.queueId = None
        self.testNum = None
        self.urlPath = None
        self.forms = None
        self.elType = None
        self.elValue = None
        self.action = None
        self.createdAt = None
        self.updatedAt = None
        BasicModule.__init__(self, dict_list, deep_split)

EL_TYPE = Enum({"1": "id", "2": "name", "3": "tag", "4": "value", "5": "selector", "6": "css"})

ACTION_TYPE = Enum({"1": "click", "2": "double click", "3": "right click", "4": "mouse over", "5": "mouse out", "6": "select"})

