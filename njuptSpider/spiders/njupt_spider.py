from scrapy import Request
from scrapy.spiders import BaseSpider
from ..items import Item, ItemTest
import pymysql

# 链接为文件的后缀名
trash = (
    'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar', 'pdf', 'ppt', 'pptx', 'pptm', 'mp3', 'jpg', 'gif', 'mp4', 'png', 'x',
    'rar')

import re

r1 = re.compile('[a-zA-z]+://[^\s]*info[0-9]*.htm$')  # 正则表达式匹配文章url
r2 = re.compile('href="/[^\s]*"')
r3 = re.compile('src="/[^\s]*"')


class NjuptSpider(BaseSpider):
    name = "njupt"
    allowed_domains = ["jwc.njupt.edu.cn"]
    start_urls = [
        "http://jwc.njupt.edu.cn/",
    ]

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', passwd='mysqlGL0111', db='urls', charset='utf8')
        self.cur = self.conn.cursor()

    def parse(self, response):
        for link in response.xpath('//a'):
            if link.xpath('@href').extract():  # 判断a标签是否有href属性
                url = link.xpath('@href').extract()[0]
                if ('mailto' in url) or ('javascript:' in url):  # 不爬取和保存邮箱链接,javascript链接
                    continue
                if 'http://' not in url:  # 将相对链接转换为绝对链接
                    url = 'http://' + response.url.split('/')[2] + url
                str = 'insert into craweled_urls (url) values '
                str += "('%s');\r\n" % (url)
                try:
                    ss = self.cur.execute(str)
                except pymysql.err.IntegrityError as e:
                    print("已爬取过的url")
                    continue
                self.conn.commit()
                if r1.match(url):
                    yield Request(url, callback=self.parse_article)
                elif (not url.lower().endswith(trash)) and (not url.startswith('http://acm')):  # 不爬取noj和文件链接
                    yield Request(url, callback=self.parse)  # 如果url合法，对该url继续爬
                else:
                    continue

    # 实现对文章页面的处理
    def parse_article(self, response):
        item = ItemTest()
        # 此处的xpath值需要根据不同的部门进行设置
        item['date'] = response.xpath("//span[@class='STYLE2']/text()").extract()[0][5:15]
        content = response.xpath('//*[@id="container_content"]/table/tr/td/table[5]').extract()[0].replace("'", '"')
        # 通过正则表达式转换相对链接为绝对链接
        for i in r2.findall(content):
            content = content.replace(i, 'href="http://' + response.url.split('/')[2] + i[6:])
        for i in r3.findall(content):
            content = content.replace(i, 'src="http://' + response.url.split('/')[2] + i[5:])
        item['content'] = content
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').extract()[0]
        item['count'] = response.url[-9:-4]
        return item
