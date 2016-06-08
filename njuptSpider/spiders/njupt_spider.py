# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
import datetime
from readability.readability import Document
import re
# 链接为文件的后缀名
from njuptSpider.items import NewsItem

urls = set([])  # 用来临时存储已经爬过的url

trash = (
    'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar', 'pdf', 'ppt', 'pptx', 'pptm', 'mp3', 'jpg', 'gif', 'mp4', 'png', 'x',
    'rar')  # 常见文件后缀

rex4url = re.compile('[a-zA-z]+://[^\s]*info[0-9]*.htm$')  # 正则表达式匹配文章url
rex4date = re.compile('info[0-9]*')  # 正则表达式匹配日期


def trans_url(content, url):
    """转换html页面内相对链接为绝对链接

    :param content:等待处理的html源码
    :param url: 页面对应的url
    :return 经过转换之后的html源码

    """
    r2 = re.compile('href="/[^\s]*"')
    r3 = re.compile('src="/[^\s]*"')

    for i in r2.findall(content):
        content = content.replace(i, 'href="http://' + url.split('/')[2] + i[6:])
    for i in r3.findall(content):
        content = content.replace(i, 'src="http://' + url.split('/')[2] + i[5:])
    return content


class NjuptSpider(Spider):
    """爬南邮的爬虫"""
    name = "njupt"
    allowed_domains = ["njupt.edu.cn"]
    start_urls = [
        "http://www.njupt.edu.cn/",
    ]

    def parse(self, response):
        """对页面进行递归爬取"""
        for link in response.xpath('//a'):
            if link.xpath('@href').extract():  # 判断a标签是否有href属性
                url = link.xpath('@href').extract()[0]  # 提取url
                if ('mailto' in url) or ('javascript:' in url):  # 不爬取和保存邮箱链接,javascript链接
                    continue
                if 'http://' not in url:  # 将相对链接转换为绝对链接
                    url = 'http://' + response.url.split('/')[2] + url
                if url in urls:  # 如果url已经爬过，不再继续爬
                    continue
                urls.add(url)  # 如果没有爬过，讲url添加到url集合中，并进行爬取
                if rex4url.match(url):
                    yield Request(url, callback=self.parse_article)
                elif (not url.lower().endswith(trash)) and (
                        not url.startswith(('http://acm',
                                            'http://xq70.njupt.edu.cn/'))):  # 不爬取noj和校庆网站
                    yield Request(url, callback=self.parse)  # 如果url合法，对该url继续爬
                else:
                    continue
            else:
                continue

    # 实现对文章页面的处理
    @staticmethod
    def parse_article(response):
        """对文章进行处理

        :param response:待处理的response
        :return: 处理之后的item对象

        """
        item = NewsItem()
        # 利用正则表达式匹配日期,部分文章页面没有日期，则用爬取时的日期代替
        try:
            item['date'] = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', response.body.decode("utf-8"))[0]
        except IndexError:
            item['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
        # 利用readability提取页面正文
        # todo 页面正文提取有待优化
        content = Document(response.body.decode('utf8')).summary(html_partial=True)
        item['url'] = response.url
        item['content'] = trans_url(content, response.url)
        item['id'] = re.findall(rex4date, response.url)[0]
        item['title'] = response.xpath('//title/text()').extract()[0]
        item['start_url'] = response.url.split('.')[0][7:]
        return item
