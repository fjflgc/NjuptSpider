# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import signals

# 经过管道将符合条件的item保存到数据库和json文件中，滤掉不符合条件的item
from scrapy.exporters import JsonItemExporter


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
        file = open('./result.json', 'w+b')
        self.files[spider] = file
        self.exporter = JsonItemExporter(file, ensure_ascii=False)  # 添加ensure_ascii=False用于使json保存中文不乱码
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        str = 'insert into showNews_news (branch,url,title) values '
        str += "('%s','%s','%s');\r\n" % (item['branch'], item['url'], item['title'])
        print(str)
        ss = self.cur.execute(str)
        self.conn.commit()  # 各种教程都没提到提交这一步啊喂!!!!!!
        self.exporter.export_item(item)
        return item
