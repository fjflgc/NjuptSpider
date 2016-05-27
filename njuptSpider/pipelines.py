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
        # 查找是否已经储存该文章，若已经储存，则进行比对和更新
        str = "select * from showNews_test WHERE url ='%s';" % item['url']
        if self.cur.execute(str):
            data = self.cur.fetchall()[0][1]
            if data != item['content']:
                # 对文章内容进行文章内容更新
                str = "update showNews_test set content=%s where url ='%s';" % (item['content'], item['url'])
                self.conn.commit()
                print("数据存在不同数据，并进行了更新")
            else:
                print("数据库中存在相同数据")
        else:
            str = 'insert into showNews_test (date,url,content,title,start_url) values '
            str += "('%s','%s','%s','%s','%s');\r\n" % (
                item['date'], item['url'], item['content'], item['title'], item['start_url'])
            ss = self.cur.execute(str)
            self.conn.commit()
        return item
