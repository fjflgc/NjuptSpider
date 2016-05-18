from scrapy import Request
from scrapy.spiders import CrawlSpider
from ..items import Item

items = []
trash = ['doc', 'docx', 'xls', 'xlsx', 'zip', 'rar', 'pdf', 'ppt', 'pptx', 'pptm', 'mp3', 'XLS', 'jpg', 'gif'];


# 实现爬南邮首页所有链接的标题和url并保存为json
class NjuptSpider(CrawlSpider):
    name = "njupt"
    allowed_domains = ["njupt.edu.cn"]
    start_urls = [
        "http://www.njupt.edu.cn/"
    ]

    def parse(self, response):  # todo 处理a标签内嵌套其他标签作为标题的情况
        for link in response.xpath('//a'):
            item = Item()
            if link.xpath('@title').extract() and link.xpath('@href').extract():  # 链接标题保存在title属性中的情况
                item['title'] = link.xpath('@title').extract()[0]
                url = link.xpath('@href').extract()[0]
                if 'njupt.edu.cn' not in url:  # 将相对链接转换为绝对链接
                    url = 'http://' + response.url.split('/')[2] + url
                item['url'] = url
                if (item in items) or ('mailto' in url) or ('javascript:' in url):  # 不爬取和保存邮箱链接,javascript链接
                    continue
                else:
                    items.append(item)
                    yield item
                    if (not url.split('.')[-1] in trash) and (not url.startswith('http://acm')):  # 不爬取noj和文件链接
                        yield Request(url, callback=self.parse)  # 如果url合法，对该url继续爬
            elif link.xpath('@href').extract() and link.xpath(
                    'text()').extract():  # 链接标题在a标签直接内部的情况 todo 想办法与第一种情况合并，减少代码重复
                item['title'] = link.xpath('text()').extract()[0]
                url = link.xpath('@href').extract()[0]
                if 'njupt.edu.cn' not in url:
                    url = 'http://' + response.url.split('/')[2] + url
                item['url'] = url
                if item in items or ('mailto' in url) or ('javascript:' in url):
                    continue
                else:
                    items.append(item)
                    yield item
                    if (not url.split('.')[-1] in trash) and (not url.startswith('http://acm')):
                        yield Request(url, callback=self.parse)
            else:
                continue

    # 实现对文章页面的处理
    def parse_article(self, response):
        pass
