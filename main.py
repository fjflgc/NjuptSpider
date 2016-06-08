# 用以支持从在pycharm中调试scrapy
from scrapy import cmdline


cmdline.execute("scrapy crawl njupt".split())
