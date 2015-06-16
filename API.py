#!/usr/bin/env python
# coding=utf-8


import suds

url = 'http://webservice.webxml.com.cn/WebServices/MobileCodeWS.asmx?wsdl'

client = suds.client.Client(url)
print client  # 结果看图1
print("-------------------------------------------------")
# result=client.service.getMobileCodeInfo(18577780801)
result = client.service.getDatabaseInfo()

print result  # 结果看图2
print("-------------------------------------------------")
print client.last_received()  # 结果看图3
