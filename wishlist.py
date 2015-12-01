#wishlist
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-01-09 15:38:50
# Project: tutorial_douban_explore

import sys
import json
import requests as reqs
import urllib2, urllib
from HTMLParser import HTMLParser
import lxml.html
import chardet
from lxml import etree 
import re
import time 
import datetime

from pyspider.database.mysql.mysqldb import SQL

from pyspider.libs.base_handler import *
from pyspider.libs.spider_wish import *

def now(formatstr):
    if formatstr == '':formatstr='%Y-%m-%d %H:%M:%S'
    d1= datetime.datetime.now()
    return d1.strftime(formatstr)

def SaveToFile(filename, content):
    f = open(filename, 'w+')
    try:
        f.write(content)
    except Exception, e:
        print Exception,":", e
    f.close()
    
    
class Handler(BaseHandler):
    '''
    js_script=function() {setTimeout("window.scrollTo(0,100000)", 1000);}
    js_script=function() {setTimeout("$('.more').click()", 1000);}
    function() {
                        window.scrollTo(0,document.body.scrollHeight);
                        setTimeout(function() { window.scrollTo(0,document.body.scrollHeight) }, 100);;
                        }
    '''
    crawl_config = {

    }
    
    _post_data = {}
    _hds = {}
    item = {}
    items = []
    def on_start(self):
        spost = SimulatePost()
        cookie = spost.login('124532043@qq.com','000000')
        print cookie
        self.crawl('https://www.wish.com/m/merchant/hourswatchcompany',
                    # fetch_type='js',
                    # js_script="""
                    # function() {
                    #   setTimeout("window.scrollTo(0,100000)", 3000);
                    # }""", 
                   # js_script="""
                   #     function() {setInterval("window.scrollTo(0,1000)", 1000);}
                   #     """,
                   callback=self.list_page, cookies = cookie, age=1*24*60*60)

              
    def list_page(self, response):
        strValue =  response.content
        SaveToFile( 'out.html', strValue)
        i=0
        for m in re.finditer(r" \"product_id\": .{0,30}\", \"",strValue):
            cid = m.group().replace(" \"product_id\": \"","").replace("\", \"","")
            i=i+1
            
            self.item['spu']=cid
            self.item['fromurl']=now('%Y%m%d')
            print self.item
            self.items.insert(i,self.item)
            self.item={}
        return self.items
                
    def on_result(self, result):
        print result
        if not result or not result[0]['spu']:
            return
        sql = SQL()
        for m in result:
            sql.replace('wishlist',**m)