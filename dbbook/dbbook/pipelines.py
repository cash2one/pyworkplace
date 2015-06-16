# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import time
import MySQLdb
import MySQLdb.cursors
import socket
import select
import sys
import os
import errno
#连接数据库
class MySQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            db = 'test',
            user = 'root',
            passwd = '000000',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = False
        )
    #pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    #错误处理
    def handle_error(self, e):
        log.err(e)



    #将每行写入数据库中
    def _conditional_insert(self, tx, item):
        if item.get('title'):
            for i in range(len(item['title'])):
                # tx.execute('insert into book values (%s, %s)', (item['title'][i], item['link'][i]))

                tx.execute("select * from book where title = %s", (item['title'][i], ))
                result = tx.fetchone()
                if result:
                    log.msg("Item already stored in db: %s" % item['title'][i], level=log.DEBUG)
                else:
                    tx.execute('insert into book values (%s, %s)', (item['title'][i], item['link'][i]))
                    log.msg("Item stored in db: %s" % item['title'][i], level=log.DEBUG)