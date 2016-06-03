# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ItemTest(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()
    content = scrapy.Field()
    start_url = scrapy.Field()
    url = scrapy.Field()