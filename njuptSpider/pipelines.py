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
        self.conn = pymysql.connect(host='localhost', user='root', passwd='root', db='njuptInfo', charset='utf8')
        self.cur = self.conn.cursor()

    def spider_closed(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # 查找是否已经储存该文章，若已经储存，则进行比对和更新
        str = "select * from ajex_text_detail WHERE id ='%s';" % item['id']
        if self.cur.execute(str):
            data = self.cur.fetchall()[0][1]
            if data != item['content']:
                # 对文章内容进行文章内容更新
                str = "update ajex_text_detail set content=%s where id ='%s';" % (item['content'], item['id'])
                self.conn.commit()
        else:
            str = 'insert into ajex_text_detail (id,content,title) values '
            str += "('%s','%s','%s');\r\n" % (
                 item['id'], item['content'],item['title'])
            str2 = 'insert into ajex_text_simple (title,date,start_url,id) values '
            str2+="('%s','%s','%s','%s');\r\n" % (item["title"],item['date'],item['start_url'],item['id'])
            try:
                self.cur.execute(str)
                self.cur.execute(str2)
            except pymysql.err.ProgrammingError as e:
                print(item['content'])
            self.conn.commit()
        return item
