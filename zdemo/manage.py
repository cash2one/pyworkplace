#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
import MySQLdb
import time

myFile = open('Table.txt', 'r')
allWords = []
line = myFile.readline()
while line:  
    getList = line.split('    ')
    for word in getList:
        if word[-1] == '\n':
            allWords.append(word[:-1])  # 去掉行末的'\n'
        else:  
            allWords.append(word) 
    line = myFile.readline()
myFile.close()

#去掉前两行
allValue =allWords[2:len(allWords)]

# print allValue[3].decode("gbk").encode("utf-8")
# values = allWords[2].decode("gbk").encode("utf-8")

# print allValue
#把一行通过 Tab分割

# print values[1].decode("gbk").encode("utf-8")
# print values
for j in range(len(allValue)):
      values=allValue[j-1].split('\t')
      try:
        conn=MySQLdb.connect(host='203.195.179.183',user='cdb_outerroot',passwd='24203cjy',port=8295,db='test',charset='utf8')
        cur=conn.cursor()
         
        # cur.execute('create database if not exists test')
        # conn.select_db('test')
          
        # value=[1,'hi rollen']
        # cur.execute('insert into book values(%s,%s)',value)
         
        # values=[]
        # for i in range(20):
        #     values.append((i,'hi rollen'+str(i)))
             
        # cur.executemany('insert into book values(%s,%s)',values)
     
        # cur.execute('update book set link="rollen" where title=3')
        
        #插入产品表
        # value=[10,'SZ',00001,'TEST','公司','行业代码A','行业名称A',20150818,20150818,1,'货币',10,'区域','状态']
        value=[10,
               values[0][0:2],
               values[0][2:8],
               values[1].decode("gbk").encode("utf-8"),
               '公司','行业代码A','行业名称A',
               '20'+time.strftime("%y%m%d"),
               '20'+time.strftime("%y%m%d"),
               1, #发布价格
               'RMB',#货币
               10, #数量
               '区域', # 区域
               '1']  #状态
        # print value
        sql='''INSERT INTO STKPRODUCT (CUNTRYCD, MARKETTPPE, STKCODE , STKNAME , 
                            CONAME, INDCODE , INDNAME , ESTBDATE, LISTDATE, IPOPRC, 
                            IPOCUR  , NSHRIPO , SCTCODE , STATCO )
                    VALUE
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
       
        cur.execute (sql ,value)
      
        #插入交易表  values[1].decode("gbk").encode("utf-8"),
        if values[6].find("--") == -1:
          status=1
        else:
          status=2
        
        value=[values[0][2:8],   # STKCODE      varchar(12)
               values[0][0:2],      # MARKETTYPE   varchar(2) '市场类型'
                '20'+time.strftime("%y%m%d"),  # TRDDATE      int(8) NOT NULL COMMENT '交易日期' ,
                values[32].replace('+',''),       # PRECLSPRC    varchar(255)  '昨日收盘价' ,
                values[30],  # OPNPRC DECIMAL (4, 4) NULL DEFAULT NULL COMMENT '日开盘价',
                values[34],       # HIPRC DECIMAL (4, 4) NULL DEFAULT NULL COMMENT '日最高价',
                values[36],         # LOPRC        decimal(4,4) NULL DEFAULT NULL COMMENT '日最低价' ,
                values[38],    # CLSPRC       decimal(4,4) NULL DEFAULT NULL COMMENT '日收盘价' ,
                values[10].replace('+',''),    # ADV DECIMAL (4, 4) NULL DEFAULT NULL COMMENT '涨跌值',
                values[6].replace('+','').replace('-',''),    # ADR          decimal(4,4) NULL DEFAULT NULL COMMENT '涨跌率 * 100' ,
                values[16],    # VOL DECIMAL (20, 0) NULL DEFAULT NULL COMMENT '日个股交易股数 成交量',
                values[53],    # AMOUNT       varchar(20) '日成交额' ,
                values[62],    # CAPITAL VARCHAR (20) '流通市值',
                values[61],    # CAPTOTAL     varchar(20) '总市值' ,
                values[42],    # PE DECIMAL (4, 2) NULL DEFAULT NULL COMMENT '市盈率',
                values[44],    #  PB           decimal(4,2) NULL DEFAULT NULL COMMENT '市净率' ,
                values[59],    # BUYVOL       decimal(10,0) NULL DEFAULT NULL COMMENT '外盘量' ,
                values[60],    # SELLVOL      decimal(10,0) NULL DEFAULT NULL COMMENT '内盘量' ,
                status   # TRDSTA       varchar(2)  '交易状态
             ]
        sql = '''INSERT INTO STKTRADE (STKCODE, MARKETTYPE, TRDDATE, PRECLSPRC,
                        OPNPRC, HIPRC, LOPRC, CLSPRC, ADV, ADR, VOL, AMOUNT,
                        CAPITAL, CAPTOTAL, PE, PB, BUYVOL, SELLVOL, TRDSTA )
                    VALUE
                      (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )'''
    
        cur.execute (sql,value)
        conn.commit()
        cur.close()
        conn.close()
        
        print "执行成功"
      except MySQLdb.Error,e:
          print "Mysql Error %d: %s" % (e.args[0], e.args[1])