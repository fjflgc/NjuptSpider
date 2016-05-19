from scrapy import Request
from scrapy.spiders import BaseSpider
from ..items import Item

urls = []
trash = (
    'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar', 'pdf', 'ppt', 'pptx', 'pptm', 'mp3', 'jpg', 'gif', 'mp4', 'png', 'x',
    'rar')
import re

r1 = re.compile('[a-zA-z]+://[^\s]*info[1-9]*.htm$')  # 正则表达式匹配文章url


# 实现爬南邮首页所有链接的标题和url并保存为json
class NjuptSpider(BaseSpider):
    name = "njupt"
    allowed_domains = ["njupt.edu.cn"]
    start_urls = [
        "http://www.njupt.edu.cn/",
        'http://iam.njupt.edu.cn/',
        'http://xjjs.njupt.edu.cn/',
        'http://iids.njupt.edu.cn/',
        'http://ipr.njupt.edu.cn/',
        'http://wcd.njupt.edu.cn/',
        'http://jxzx.njupt.edu.cn/',
        'http://lib.njupt.edu.cn/',
        'http://dag.njupt.edu.cn/',
        'http://qks.njupt.edu.cn/',
    ]

    def parse(self, response):  # todo 处理a标签内嵌套其他标签作为标题的情况
        for link in response.xpath('//a'):
            item = Item()
            if link.xpath('@href').extract():  # 判断a标签是否有href属性
                url = link.xpath('@href').extract()[0]
                if 'http://' not in url:  # 将相对链接转换为绝对链接
                    url = 'http://' + response.url.split('/')[2] + url
                item['url'] = url
                item['branch'] = response.url.split('/')[2]
                if link.xpath('@title').extract():
                    item['title'] = link.xpath('@title').extract()[0]
                elif link.xpath(
                        'string(.)').extract():
                    item['title'] = link.xpath('string(.)').extract()[0]
                else:
                    continue
                if (url in urls) or ('mailto' in url) or ('javascript:' in url):  # 不爬取和保存邮箱链接,javascript链接
                    continue
                else:
                    urls.append(url)
                    if r1.match(url):
                        yield item
                    elif (not url.lower().endswith(trash)) and (not url.startswith('http://acm')):  # 不爬取noj和文件链接
                        yield Request(url, callback=self.parse)  # 如果url合法，对该url继续爬
            else:
                continue

    # 实现对文章页面的处理
    def parse_article(self, response):
        pass
