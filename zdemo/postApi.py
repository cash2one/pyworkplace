#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import hashlib
from operator import itemgetter


from urllib import urlencode

def md5(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()
def sortedDictValues1(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items] 
def my_urlencode(str) :
    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]

session = requests.Session()
url_post = "https://apis.chinabrands.com/app_login_api.php"
client_secret='8784c11b8723b92ed24b76c84a831315'


postdata = {
    'email': 'i@imcfy.com',
    'password': '000000',
    'client_id': '7781809591',
}

#转成字符串格式
# strpost=''
# for key, value in postdata.items():
#     strpost += "\"%s\":\"%s\"" % (key, value) +','
# str='{'+strpost[0:-1]+'}'
# print str

# data_sort = sorted(postdata.iteritems(), key=itemgetter(1), reverse=True)#排序
# print data_sort
#转json
json_data = json.dumps(postdata,sort_vlue=True)
#加密
signature_string=md5(json_data+client_secret)
print json_data+client_secret
params = urlencode( {'data': json.dumps(json_data)})

post_data= 'signature='+signature_string+'&'+params
print post_data
resp = session.post(url_post,data=post_data)
print resp.text