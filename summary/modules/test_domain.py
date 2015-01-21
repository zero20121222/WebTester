# coding=utf-8
# Date=1/17/15
__author__ = 'MichaelZhao'

from summary.modules.basic_module import BasicModule

'''
--
CREATE TABLE `test_domains` (
  `id`                 BIGINT(20)        NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `domain`             VARCHAR(128)      NOT NULL COMMENT 'domain',
  `created_at`         DATETIME          NOT NULL COMMENT '创建时间',
  `updated_at`         DATETIME          NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
);
CREATE INDEX `test_domains_domain` ON test_domains(`domain`);
'''
class TestDomain(BasicModule):
    def __init__(self, dict_list=None, deep_split=False):
        self.id = None
        self.domain = None
        self.createdAt = None
        self.updatedAt = None
        BasicModule.__init__(self, dict_list, deep_split)