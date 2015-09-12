#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import hashlib
from urllib import urlencode

def md5(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()
def sortedDictValues1(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items] 
    
session = requests.Session()
url_post = "https://apis.chinabrands.com/app_login_api.php"

client_secret='8784c11b8723b92ed24b76c84a831315'


postdata = {
    'email': 'i@imcfy.com',
    'password': '000000',
    'client_id': '7781809591',
}
str='{"email":"i@imcfy.com","password":"000000","client_id":"7781809591"}'
str='{"password":"000000","email":"i@imcfy.com","client_id":"7781809591"}'

signature_string=md5(str+client_secret)

post_data='signature=5a727049a77aeca909582667f0030a27&data=%7B%22email%22%3A%22i%40imcfy.com%22%2C%22password%22%3A%22000000%22%2C%22client_id%22%3A%227781809591%22%7D'
print postdata
print sortedDictValues1(postdata)
print urlencode(postdata)
print post_data
resp = session.post(url_post,data=post_data)
print resp.text