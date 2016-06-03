from scrapy import Request
from scrapy.spiders import BaseSpider
from ..items import ItemTest
import datetime
import pymysql
import re
from readability.readability import Document
# 链接为文件的后缀名
urls = set([])

trash = (
    'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar', 'pdf', 'ppt', 'pptx', 'pptm', 'mp3', 'jpg', 'gif', 'mp4', 'png', 'x',
    'rar')

import re

r1 = re.compile('[a-zA-z]+://[^\s]*info[0-9]*.htm$')  # 正则表达式匹配文章url
r2 = re.compile('href="/[^\s]*"')
r3 = re.compile('src="/[^\s]*"')
r4 = re.compile('info[0-9]*')

class NjuptSpider(BaseSpider):
    name = "njupt"
    allowed_domains = ["njupt.edu.cn"]
    start_urls = [
        "http://www.njupt.edu.cn/",
        "http://jwc.njupt.edu.cn/"
    ]

    def parse(self, response):
        for link in response.xpath('//a'):
            if link.xpath('@href').extract():  # 判断a标签是否有href属性
                url = link.xpath('@href').extract()[0]
                if ('mailto' in url) or ('javascript:' in url):  # 不爬取和保存邮箱链接,javascript链接
                    continue
                if 'http://' not in url:  # 将相对链接转换为绝对链接
                    url = 'http://' + response.url.split('/')[2] + url
                if url in urls:
                    continue
                urls.add(url)
                if r1.match(url):
                    yield Request(url, callback=self.parse_article)
                elif (not url.lower().endswith(trash)) and (
                        not url.startswith(('http://acm', 'http://xq70.njupt.edu.cn/'))):  # 不爬取noj和文件链接
                    yield Request(url, callback=self.parse)  # 如果url合法，对该url继续爬
                else:
                    continue
            else:
                continue

    # 实现对文章页面的处理
    def parse_article(self, response):
        item = ItemTest()
        # 利用正则表达式匹配日期
        try:
            item['date'] = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', response.body.decode("utf-8"))[0]
        except IndexError:
            item['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        # 转换相对链接为绝对链接
        content = Document(response.body.decode('utf8')).summary(html_partial=True)
        for i in r2.findall(content):
            content = content.replace(i, 'href="http://' + response.url.split('/')[2] + i[6:])
        for i in r3.findall(content):
            content = content.replace(i, 'src="http://' + response.url.split('/')[2] + i[5:])
        item['url'] = response.url
        item['content'] = content
        item['id'] = re.findall(r4, response.url)[0]
        item['title'] = response.xpath('//title/text()').extract()[0]
        item['start_url'] = response.url.split('.')[0][7:]
        return item
