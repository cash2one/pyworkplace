#coding=utf-8
__author__ = 'cfy'
"""
Date: 2015-6-15
"""

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule		#这个是预定义的蜘蛛，使用它可以自定义爬取链接的规则rule
from scrapy.selector import HtmlXPathSelector			   #导入HtmlXPathSelector进行解析
from dbbook.items import DbbookItem
f=open('log.txt','a')
class firstScrapy(CrawlSpider):
  name = "book"									#爬虫的名字要唯一
  allowed_domains = ["http://stock.hexun.com/"]				   #运行爬取的网页
  start_urls = ["http://stock.hexun.com/"]   #第一个爬取的网页
#   start_urls = ["http://yuedu.baidu.com/book/list/0?od=0&show=1"]
#   #以下定义了两个规则，第一个是当前要解析的网页，回调函数是myparse；第二个则是抓取到下一页链接的时候，不需要回调直接跳转
#   rules = [Rule(SgmlLinkExtractor(allow=('/ebook/[^/]+fr=booklist')), callback='myparse'),
#       Rule(SgmlLinkExtractor(allow=('/book/list/[^/]+pn=[^/]+', )), follow=True)]

  #回调函数
  def myparse(self, response):
    x = HtmlXPathSelector(response)
    item = DbbookItem()

    # get item
    item['link'] = response.url
    item['title'] = ""
    
    f.write(str(item['link']+'\r\n'))
    strlist = x.select("/x:html/x:body/x:div[11]/x:div[1]/x:h1/x:a[2]/x:strong").extract()
    if len(strlist) > 0:
      item['title'] = strlist[0]
    
    return item
