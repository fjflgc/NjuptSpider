# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    branch = scrapy.Field()


class ItemTest(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    content  = scrapy.Field()
    count = scrapy.Field()