__author__ = 'cfy'
# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from dbstock.items import productItem
 
class product(BaseSpider):
   name = "stkproduct"
   allowed_domains = ["gu.qq.com"]
   start_urls = ["http://gu.qq.com/sz000100"]


   def parse(self, response):
      hxs = HtmlXPathSelector(response)
      item = productItem()
     
      item['CUNTRYCD'] = '10' # '国家代码    
      item['STKCODE'] = '000100'   # '证券代码',
      item['STKNAME'] = hxs.select('id(''mod-hqpanel'')/x:div[1]/x:div[1]/x:h1[1]').extract()
      item['CONAME'] = ''  #'公司名称',
      item['INDCODE'] = ''  # '行业代码A',
      item['INDNAME'] = ''  # '行业名称A',
      item['NINDCOME'] = ''  # '行业代码B',
      item['NINDNAME'] = ''  # '行业名称B',
      item['ESTBDATE'] = ''  #'公司成立日期',
      item['LISTDATE'] = ''  #  '上市日期',
      item['IPOPRC'] = ''  # '发行价格',
      item['IPOCUR'] = ''  # '发行货币 发行价格的计量货币   
      item['NSHRIPO'] = ''  # '发行数量',
      item['SCTCODE'] = ''  # '区域码 1=上海，2=深圳',
      item['STATCO'] = ''  # '公司活动情况  
      item['MARKETTPPE'] = ''  # '市场类型       
    
    
      print '---------------------------------------------' + item['STKNAME']
      yield item
      