from scrapy.spiders import CrawlSpider
from ..items import Item
items = []

# 实现爬南邮首页所有链接的标题和url并保存为json
class NjuptSpider(CrawlSpider):
    name = "njupt"
    allowed_domains = ["njupt.edu.cn"]
    start_urls = [
        "http://www.njupt.edu.cn/"
    ]

    def parse(self, response):
        for link in response.xpath('//a'):
            item = Item()
            if link.xpath('@title').extract() and link.xpath('@href').extract():
                item['title'] = link.xpath('@title').extract()[0]
                url = link.xpath('@href').extract()[0]
                if 'http' not in url:
                    url = 'http://www.njupt.edu.cn' + url
                item['url'] = url
                if item in items:
                    continue
                items.append(item)
                yield item
            else:
                continue
