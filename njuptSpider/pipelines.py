# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import signals
# 经过管道将符合条件的item保存到数据库中，滤掉不符合条件的item

class Pipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.conn = pymysql.connect(host='localhost', user='root', passwd='mysqlGL0111', db='njuptInfo', charset='utf8')
        self.cur = self.conn.cursor()

    def spider_closed(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        str = 'insert into showNews_test (date,url,content,title,count) values '
        str += "('%s','%s','%s','%s','%s');\r\n" % (
            item['date'], item['url'], item['content'], item['title'], item['count'])
        try:
            ss = self.cur.execute(str)
        except pymysql.err.IntegrityError as e:
            print("数据库中已存在的文章")
        self.conn.commit()  # 各种教程都没提到提交这一步啊喂!!!!!!
        return item
