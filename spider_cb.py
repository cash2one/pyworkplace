#jobs_github
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-27 09:02:11
# Project: jobs_coreint

from pyspider.database.mysql.mysqldb import SQL
from pyspider.libs.base_handler import *
from pyspider.libs.cbspider import *
import sys
import json
import requests as reqs
import urllib2, urllib
from HTMLParser import HTMLParser
from lxml import etree 
import chardet
import os
import re
import time 
import datetime

from sevencow import CowException
from sevencow import CowException

tmp_dict = {}
out_dict = {}
out_list = []


def now(formatstr):
    if formatstr == '':formatstr='%Y-%m-%d %H:%M:%S'
    d1= datetime.datetime.now()
    return d1.strftime(formatstr)

def login(url, username, password):
    rqs = reqs.Session()
    rsps = rqs.get(url)

    cookies = ''
    for index, cookie in enumerate(rqs.cookies):
        cookies = cookies+cookie.name+"="+cookie.value+";";
    print 'cookies: ',cookies
    # print 'Code: ',cookie.value

    cCode = cookie.value
    # self._post_data.setdefault('checkCode',cCode)
    
    
    _post_data = {'email':username, 'password':password}
    _hds = {
            'Host':'www.chinabrands.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
            'Accept':'text/plain, */*; q=0.01',
            'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest',
            'Referer':'http://www.chinabrands.com/m-users-a-sign.htm',
            'Content-Length':'43',
            'Cookie':cookies,
            'Connection':'keep-alive',
            'Pragma':'no-cache',
            'Cache-Control':'no-cache',
          }


    #发送post请求
    posturl = 'http://www.chinabrands.com/m-users-a-act_sign.htm'
    postdata = urllib.urlencode(_post_data)


    rsps = rqs.post(posturl, data = postdata, headers=_hds)
    print rsps.content 
    dictcookies={}
    for index, cookie in enumerate(rqs.cookies):
        cookies = cookies+cookie.name+"="+cookie.value+";";
        dictcookies[cookie.name]=cookie.value
    # print 'cookies: ',cookies
    return dictcookies


def createDict(response, tmp_dict, color, size):
    descv =  '' if  response.doc('div.chart-table').html() == None else response.doc('div.chart-table').html()
    tmp_out_dict = {
                "id": '',
                "spu": 'CB_P'+response.doc('#goodsSKU\\20 mt5\\20 mb5').text()[:-2],
                "sku": 'CB_P'+response.doc('#goodsSKU\\20 mt5\\20 mb5').text()+color+size,
                "title": response.doc('#h1_goodsTitle > h1').text(),
                "description": response.doc('#goods_desc').html() + descv,
                "tag": '1,' ,
                "brand": "CB",
                "upc": "",
                "lpurl": "",
                "msrp":response.doc('#unit_price2').text(),
                "color": color,
                "size": size,
                "fromurl": response.url,
                "price": response.doc('#unit_price2').text() ,
                "shipfree": response.doc('#main0>div.js_showtable.none.shipping_cost_desc>div:nth-child(2)>table>tbody>tr:nth-child(3)>td:nth-child(7)').text(),
                "quantity": int("688"),
                "minday": int("25"),
                "maxday":int("40"),
                "mainimgurl": tmp_dict['imgurl0'],
                "imgurl1": tmp_dict['imgurl1'],
                "imgurl2": tmp_dict['imgurl2'],
                "imgurl3": tmp_dict['imgurl3'],
                "imgurl4": tmp_dict['imgurl4'],
                "imgurl5": tmp_dict['imgurl5'],
                "imgurl6": tmp_dict['imgurl6'],
                "imgurl7": tmp_dict['imgurl7'],
                "imgurl8": tmp_dict['imgurl8'],
                "imgurl9": tmp_dict['imgurl9'],
                "imgurl10": tmp_dict['imgurl10'],
                "note": "",
                "srcsys": "CB",
                "inserttime": now(''),
            }
    # print 'tmp_out_dict',tmp_out_dict
    return tmp_out_dict

class Handler(BaseHandler):
    crawl_config = {
    }
    @every(minutes=24 * 60)
    def on_start(self):

        #cookies=login('http://www.chinabrands.com/m-users-a-sign.htm','125769692@qq.com','xlq890210')
        self.crawl('http://www.chinabrands.com/Wholesale-3G-smart-Phones-c-31.html', callback=self.index_page)

    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://www.chinabrands.com/product\d', each.attr.href):
                self.crawl(each.attr.href+'#more', callback=self.index_page_color  , age=1*24*60*60)
        for each in response.doc('#classmain>div.xbpagelei>div>p.listspan>a:nth-child(8)').items():
            self.crawl(each.attr.href, callback=self.index_page,   age=1*24*60*60)

    def index_page_color(self, response):
        slogin = SimulatePost()


        tree=etree.HTML(response.content)
        nodesv=tree.xpath(u"id('bodymain2')/div[4]/div[1]/div[2]/p[5]/select/option/@value")
        nodesi=tree.xpath(u"id('bodymain2')/div[4]/div[1]/div[2]/p[5]/select/option")
        #------------no  color  -----------------------------
        if nodesv == [] :
            imgDict = slogin.dict_img(response.content,0)
            self.crawl(response.url, callback=self.detail_page,  save={'color': '','imgdict':imgDict}, age=1*24*60*60)
        #---------have color -------------------------
        else:
            imgDict = slogin.dict_img(response.content)
            for i in range(len(nodesv)):
                if nodesv[i] == '' :
                    continue 
                _color =''.join(nodesi[i].text.split())
                print str(i-1),slogin.get_imgurl('http://www.chinabrands.com/product'+nodesv[i]+'.html')
                imgDict['imgurl'+str(i-1)] = slogin.get_imgurl('http://www.chinabrands.com/product'+nodesv[i]+'.html')
                print '1 color :', _color
                self.crawl('http://www.chinabrands.com/product'+nodesv[i]+'.html', callback=self.detail_page, save={'color': _color ,'imgdict':imgDict}, age=1*24*60*60)

    @config(priority=2)
    def detail_page(self, response):
        global tmp_dict
        global out_dict
        global out_list

        tree=etree.HTML(response.content)
        nodes_sv=tree.xpath(u"id('bodymain2')/div[4]/div[1]/div[2]/p[6]/select/option")
        nodes_sn=tree.xpath(u"id('bodymain2')/div[4]/div[1]/div[2]/p[6]/select/@name")
        #------------have size -------
        if len(nodes_sn) == 0 :
            print '------  no  size'
            out_dict = {}  
            print '2 color :', response.save['color']
            out_dict = dict( out_dict,**createDict(response, response.save['imgdict'], response.save['color'], ''))
            out_list.append(out_dict) # add to list
        elif  nodes_sn[0] == 'select_same_goods_63':
            print '------- have size'
            for m in nodes_sv:
                # print 'Size VALUE: ', ''.join(m.text.split())
                if  ''.join(m.text.split()) == 'Pleaseselect...':
                    continue
                out_dict = {}   
                print '2 color :',response.save['color']
                out_dict = dict( out_dict, **createDict(response, response.save['imgdict'], response.save['color'], ''.join(m.text.split())) )
                out_list.append(out_dict) # add to list
        #-----no size ----------------
        else :
            print '------  no  size'
            out_dict = {}  
            print '2 color :', response.save['color']
            out_dict = dict( out_dict,**createDict(response, response.save['imgdict'], response.save['color'], ''))
            out_list.append(out_dict) # add to list
        return out_list

    def on_result(self, result):
        print result
        if not result or not result[0]['spu']:
            return
        sql = SQL()
        for values in result:
            sql.replace('wish',**values)