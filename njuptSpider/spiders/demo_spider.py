from scrapy.spider import Spider

class DemoSpider(Spider):
	name = "njuptIndexSpider"
	allowed_domains = ["njupt.edu.cn"]
	start_urls = [
		"http://www.njupt.edu.cn/"
	]
	def parse(self,response):
		filename = response.url.split("/")[-2]
		with open(filename, 'wb') as f:
			f.write(response.body)