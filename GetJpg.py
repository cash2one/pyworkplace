__author__ = 'cfy'
# !/usr/bin/env python
# coding=utf-8

import urllib
import re

import urllib
import re
import os


def downloadPage(url):
    h = urllib.urlopen(url)
    return h.read()


def downloadimg(content):

    pattern = r'src="(.+?\.jpg)" pic_ext'
    m = re.compile(pattern)
    urls = re.findall(m, content)
    for i, url in enumerate(urls):
        local = os.path.join('/home/cfy/Pictures', "%s.jpg" % (i, ))
        urllib.urlretrieve(url, local)


content = downloadPage("http://tieba.baidu.com/p/2460150866")
downloadimg(content)