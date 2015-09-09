#!/usr/bin/python
#  coding:utf-8
import requests, json

url = "http://sendcloud.sohu.com/webapi/mail.send.json"

params = {"api_user": "imcfy_test_hobrIj",
          "api_key": "59aUXguhKxH0Ejyw",
          "from": "service@sendcloud.im",
          "fromname": "SendCloud",
          "to": "i@imcfy.com",
          "subject": "test",
          "html": "test",
          "resp_email_id": "true"
          }

r = requests.post(url, files={}, data=params)
print r.text