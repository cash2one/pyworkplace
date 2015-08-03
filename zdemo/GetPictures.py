# coding=utf-8
import urllib
import re
import os

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    x = 0
    for imgurl in imglist:
        local = os.path.join('/home/ubuntu/workspace/pictures','%s.jpg' % x)
        urllib.urlretrieve(imgurl,local)
        x += 1


html = getHtml("http://tieba.baidu.com/p/2460150866")

print getImg(html)
print ('GetImg succeeded')