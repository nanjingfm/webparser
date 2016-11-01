# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from hashlib import md5

class MySQLStorePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        linkhash = self._get_linkhash(item)
        conn.execute("select 1 from aaa where linkhash = %s", (linkhash,))
        ret = conn.fetchone()

        if ret:
            conn.execute("""
                update aaa set `name` = %s, linkurl = %s, imageurl = %s, updatetime = %s where linkhash = %s
            """, (item['name'], item['link'], item['imageurl'], item['updatetime'], linkhash))
        else:
            conn.execute("""
                insert into aaa(`name`, linkurl, imageurl, updatetime, linkhash)
                values(%s, %s, %s, %s, %s)
            """, (item['name'], item['link'], item['imageurl'], item['updatetime'], linkhash))

    # 获取url的md5编码
    def _get_linkhash(self, item):
        return md5(item['link']).hexdigest()

    # 异常处理
    def _handle_error(self, failue, item, spider):
        print("error")