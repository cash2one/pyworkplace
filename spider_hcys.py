#valsun
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-23 17:27:03
# Project: valsun
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
from pyspider.libs.login_hcys import *
from pyspider.libs.login_hcys_img import *


_loginFlag=0
_descJson = ""


def now(formatstr):
    d1= datetime.datetime.now()
    return d1.strftime(formatstr)

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
def main(username,pwd,productSpu, flag):
    simg = SimulateImg()
    if flag ==0 :
        print ('-----------------执行登陆功能------------------')
        resultValue = simg.login('http://ali.pics.valsun.cn/v1/login.php',username,pwd)
        if resultValue == 0 : main(username,pwd,productSpu,flag)
    
    print ('-----------------执行打印水印------------------')
    simg.waterMark('http://ali.pics.valsun.cn/v1/addWaterByUser.php',productSpu,'615|1141|Ambergris')
    
    print ('-----------------执行下载功能------------------')
    simg.downImg('http://ali.pics.valsun.cn/v1/addWaterByUserHistory.php','/home/downImg/'+productSpu+'.zip')
    
    print ('-----------------执行上传图片------------------')
    return simg.uploadPhotos(1,'/home/downImg/picture/'+productSpu)

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        username = 'i@imcfy.com'
        password = 'imcfy000000'

        slogin = SimulateLogin()
        cookies=slogin.login('http://www.valsun.cn/index.php?mod=login&act=login','i@imcfy.com','imcfy000000')

        self.crawl('http://www.valsun.cn/index.php?mod=product&act=detail&sku=10049_C', callback=self.index_page,
             method='GET', cookies = cookies)

    
    def index_page(self, response):
        self.crawl('http://www.valsun.cn/index.php?mod=goods&act=list&status=1&is_new=9&goodsname=&category_one=5&CateName=5&category_two=5-36&CateName=5-36', callback=self.list_page, cookies = response.cookies)

    #@config(age=24 * 60 * 60)
    def list_page(self, response):
        for each in response.doc('html>body>div.v2Main>div.v2typeSel>div.v2typeList>ul>li.tit>a').items():
            self.crawl(each.attr.href, callback=self.detail_page,cookies = response.cookies)
        for each in response.doc('html>body>div.v2Main>div.v2typeSel>div.ui-Page-Fbm>ul>span.page>a.lastpage').items():
            self.crawl(each.attr.href,callback=self.list_page,cookies = response.cookies)


    @config(priority=2)
    def detail_page(self, response):
        
        
        

        global _loginFlag 
        global _descJson

        tree=etree.HTML(response.content)
        nodes=tree.xpath(u"//ul[11]/li[2]")

        patt = re.compile(r"(\d+\.\d+)")
        m = patt.search(nodes[0].text)

        patt1 = re.compile(r"快递 : \d+\.*\d*")
        m1 = patt1.search(response.content)
        price = round(float(m.group()),4)+ round(float(m1.group()[9:]),4)

        pruductSpu =response.doc('div.listmyorder-right>div.prodetpage>ul:nth-child(2)>li.pro_right').text()

        rsps = reqs.get('http://www.valsun.cn/index.php?mod=product&act=findDescBySPU&spu=' + pruductSpu,cookies = response.cookies)
        dict = rsps.json()
        _descJson=dict['html']
        print 'pruductSpu: ',pruductSpu
        listImgUrl = main('i@imcfy.com','imcfy000000',pruductSpu,_loginFlag)
        print 'len(listImgUrl)',len(listImgUrl)
        if len(listImgUrl ) != 0 :
            _loginFlag=1

        SaveToFile('content.txt',response.json)
        return {
            "id": '',
            "spu": 'valsum_'+response.doc('div.listmyorder-right>div.prodetpage>ul:nth-child(2)>li.pro_right').text(),
            "sku": 'valsum_'+response.doc('div.listmyorder-right>div.prodetpage>ul:nth-child(3)>li.pro_right').text(),
            "title": response.doc('div.listmyorder-right>div.prodetpage>ul:nth-child(6)>li.pro_right').text(),
            "description": _descJson,
            "tag": '111,222',
            "brand": "HCYS",
            "upc": "",
            "lpurl": "",
            "msrp":price,
            "color": "",
            "size":response.doc('div.listmyorder-right>div.prodetpage>ul:nth-child(10)>li.pro_right').text(),
            "fromurl": response.url,
            "price": price ,
            "shipfree": int("4"),
            "quantity": int("1200"),
            "minday": int("25"),
            "maxday":int("40"),
            "mainimgurl": listImgUrl[[len(listImgUrl)-1,0][len(listImgUrl)>1]],
            "imgurl1": listImgUrl[[len(listImgUrl)-1,1][len(listImgUrl)>1]],
            "imgurl2": listImgUrl[[len(listImgUrl)-1,2][len(listImgUrl)>2]],
            "imgurl3": listImgUrl[[len(listImgUrl)-1,3][len(listImgUrl)>3]],
            "imgurl4": listImgUrl[[len(listImgUrl)-1,4][len(listImgUrl)>4]],
            "imgurl5": listImgUrl[[len(listImgUrl)-1,5][len(listImgUrl)>5]],
            "imgurl6": listImgUrl[[len(listImgUrl)-1,6][len(listImgUrl)>6]],
            "imgurl7": listImgUrl[[len(listImgUrl)-1,7][len(listImgUrl)>7]],
            "imgurl8": listImgUrl[[len(listImgUrl)-1,8][len(listImgUrl)>8]],
            "imgurl9": listImgUrl[[len(listImgUrl)-1,9][len(listImgUrl)>9]],
            "imgurl10": listImgUrl[[len(listImgUrl)-1,10][len(listImgUrl)>10]],
            "note": "",
            "srcsys": "HCYS",
            "inserttime": now(''),
        }
    def on_result(self, result):
        print result
        if not result or not result['spu']:
            return
        sql = SQL()
        sql.replace('wish',**result)