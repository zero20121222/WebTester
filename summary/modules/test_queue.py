# coding=utf-8
# Date=1/17/15
__author__ = 'MichaelZhao'

from summary.modules.basic_module import BasicModule

'''
--
CREATE TABLE `test_queues` (
  `id`                 BIGINT(20)        NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `queue_name`         VARCHAR(128)      NOT NULL COMMENT 'name',
  `created_at`         DATETIME          NOT NULL COMMENT '创建时间',
  `updated_at`         DATETIME          NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
);
CREATE INDEX `test_queues_queue_name` ON test_queues(`queue_name`);
'''
class TestQueue(BasicModule):
    def __init__(self, dict_list=None, deep_split=False):
        self.id = None
        self.queueName = None
        self.createdAt = None
        self.updatedAt = None
        BasicModule.__init__(self, dict_list, deep_split)