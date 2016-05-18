# NjuptSpider
实现递归爬取njupt.edu.cn域名下所有链接的标题和url并保存到项目根目录的result.json文件中

运行方法：用pycharm直接运行或者在根目录直接终端运行scrapy crawl njupt

已知问题：

- 无法保存形如'<a href='baidu.com'><font>链接标题</font></a>'的在a标签内嵌套其他标签的链接

- 无法增量爬取，且一次爬取需要耗费较长时间