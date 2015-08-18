#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
import MySQLdb
 
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
    values=[10,'SZ',00001,'TEST','公司','行业代码A','行业名称A',20150818,20150818,1,'货币',10,'区域','状态']
    sql='''INSERT INTO STKPRODUCT (CUNTRYCD, MARKETTPPE, STKCODE , STKNAME , 
                        CONAME, INDCODE , INDNAME , ESTBDATE, LISTDATE, IPOPRC, 
                        IPOCUR  , NSHRIPO , SCTCODE , STATCO )
                VALUE
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
   
    cur.execute (sql ,values)
    
    #插入交易表
    values=['00001',   # STKCODE      varchar(12)
            'SZ',      # MARKETTYPE   varchar(2) '市场类型'   
            20150818,  # TRDDATE      int(8) NOT NULL COMMENT '交易日期' ,
            1.1,       # PRECLSPRC    varchar(255)  '昨日收盘价' ,
            1111.1000,  # OPNPRC DECIMAL (4, 4) NULL DEFAULT NULL COMMENT '日开盘价',
            1.2,       # HIPRC DECIMAL (4, 4) NULL DEFAULT NULL COMMENT '日最高价',
            1,         # LOPRC        decimal(4,4) NULL DEFAULT NULL COMMENT '日最低价' ,
            1.3,    # CLSPRC       decimal(4,4) NULL DEFAULT NULL COMMENT '日收盘价' ,
            1,    # ADV DECIMAL (4, 4) NULL DEFAULT NULL COMMENT '涨跌值',
            2,    # ADR          decimal(4,4) NULL DEFAULT NULL COMMENT '涨跌率 * 100' ,
            20,    # VOL DECIMAL (20, 0) NULL DEFAULT NULL COMMENT '日个股交易股数 成交量',
            '20',    # AMOUNT       varchar(20) '日成交额' ,
            '1',    # CAPITAL VARCHAR (20) '流通市值',
            '33',    # CAPTOTAL     varchar(20) '总市值' ,
            44,    # PE DECIMAL (4, 2) NULL DEFAULT NULL COMMENT '市盈率',
            66,    #  PB           decimal(4,2) NULL DEFAULT NULL COMMENT '市净率' ,
            77,    # BUYVOL       decimal(10,0) NULL DEFAULT NULL COMMENT '外盘量' ,
            88,    # SELLVOL      decimal(10,0) NULL DEFAULT NULL COMMENT '内盘量' ,
            '1'   # TRDSTA       varchar(2)  '交易状态   
         ]
    sql = '''INSERT INTO STKTRADE (STKCODE, MARKETTYPE, TRDDATE, PRECLSPRC, 
                    OPNPRC, HIPRC, LOPRC, CLSPRC, ADV, ADR, VOL, AMOUNT, 
                    CAPITAL, CAPTOTAL, PE, PB, BUYVOL, SELLVOL, TRDSTA )
                VALUE
                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )'''  
	
    cur.execute (sql,values)
    conn.commit()
    cur.close()
    conn.close()
    
    # print sql,values 
except MySQLdb.Error,e:
    
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])