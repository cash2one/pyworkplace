from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from dbbook.items import DmozItem
 
class DmozSpider(BaseSpider):
   name = "dmoz"
   allowed_domains = ["dmoz.org"]
   start_urls = [
       "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
       "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
   ]


   # def parse(self, response):
   #      items=[]
   #      for sel in response.xpath('//ul/li'):
   #          item = DmozItem()
   #          item['title'] = sel.xpath('a/text()').extract()
   #          item['link'] = sel.xpath('a/@href').extract()
   #          item['desc'] = sel.xpath('text()').extract()
   #          items.append(item)
   #      return items



   def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item

