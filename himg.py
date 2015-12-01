#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-27 09:02:11
# Project: jobs_coreint

from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup
import re
import os
import uuid
import urllib


listPicName=''
localPath=''
urlList=[] 
#从一个网页url中获取图片的地址，保存在  
#一个list中返回  
def getUrlList(getContent):  

    htmlString = getContent
    if( len(htmlString)!=0 ):  
        patternString=r"http://.*\.jpg"  
        searchPattern=re.compile(patternString)  
        imgUrlList=searchPattern.search(htmlString)  
        return imgUrlList  

#生成一个文件名字符串   
def generateFileName():  
    return str(uuid.uuid1())  
  
      
#根据文件名创建文件    
def createFileWithFileName(localPathParam,fileName):
    if not os.path.exists(localPathParam):
        os.mkdir(localPathParam)
    totalPath=localPathParam+fileName  
    if not os.path.exists(totalPath):  
        file=open(totalPath,'a+')  
        file.close()  
        return totalPath  
      
  
#根据图片的地址，下载图片并保存在本地   
def getAndSaveImg(imgUrl):  
    if( len(imgUrl)!= 0 ):  
        fileName=generateFileName()+'.jpg'  
        urllib.urlretrieve(imgUrl,createFileWithFileName(localPath,fileName))
        return fileName
  
#下载函数  
def downloadImg(content):  
    global  urlList
    global listPicName
    htmlString = content
    if( len(htmlString)!=0 ):  
        patternString=r"http://pic\..{0,50}\.jpg"
        searchPattern=re.compile(patternString)  
        imgUrlList=searchPattern.findall(htmlString)  
   
    for urlString in imgUrlList:
        print urlString
        PicName = getAndSaveImg(urlString)  
        listPicName =listPicName + ";"+PicName
    return listPicName

class Handler(BaseHandler):
    crawl_config = {
        "headers": {
            "Referer": "http://www.y171.com/", 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0", 
        }
    }
       

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.y171.com/', callback=self.index_page)


    #@config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://.*/htm/piclist\d\/', each.attr.href):
                self.crawl(each.attr.href, callback=self.index_page2)


    @config(age=10 * 24 * 60 * 60)
    def index_page2(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://.*/htm/pic\d\/', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('body>div.wrap.mt10>div.wrap.mt10>div>div.pagination>a:nth-child(12)').items():
            self.crawl(each.attr.href,callback=self.index_page2)



    @config(priority=2)
    def detail_page(self, response):
        global localPath

        #create filepath
        # if os.path.exists('/home/data/Himg/') == False :
        #     os.mkdir(r'/home/data/Himg')
        localPath='/home/data/Himg/'

        listPicName1=downloadImg(response.content) 
        
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "listPicName": listPicName1
        }
