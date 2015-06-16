__author__ = 'cfy'
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
# from second.items import bbs
from dbbook.items import DbbookItem

class bbsSpider(BaseSpider):
    name = "boat"
    allow_domains = ["http://book.douban.com/tag/编程?type=S"]
    start_urls = ["http://book.douban.com/tag/编程?type=S"]
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        item = DbbookItem()
        item['title'] = hxs.select('//ul/li[position()>0]/div[2]/h2/a/@title').extract()
        item['link'] = hxs.select('//ul/li[position()>0]/div[2]/h2/a/@href').extract()
        items.append(item)
        return items
    # scrapy crawl boat -o book_data.json