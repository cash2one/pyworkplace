# -*- coding: utf-8 -*-
import xdrlib, sys
import xlrd
import MySQLdb
import time
# import sys


def open_excel(file='Table1.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception, e:
        print str(e)


def iif(condition, true_part, false_part):
    return (condition and [true_part] or [false_part])[0]


# 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file='Table1.xls', colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  #行数
    ncols = table.ncols  #列数
    colnames = table.row_values(colnameindex)  #某一行数据
    list = []
    for rownum in range(1, nrows):

        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file='Table1.xls', colnameindex=0, by_name=u'sql'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows  #行数
    colnames = table.row_values(colnameindex)  #某一行数据
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list

# def main():
#    tables = excel_table_byindex()
#    for row in tables:
#        return list(row)

#   tables = excel_table_byname()
#   for row in tables:
#       print row
if __name__ == "__main__":
        #处理传入进来的日期
    if  len(sys.argv) == 1:
        skDate ='20' + time.strftime("%y%m%d")
    else:
        skDate =sys.argv[1]

    tables = excel_table_byindex('Table'+skDate+'.xls')
    rn=0



    print skDate
    for row in tables:
        rn += 1
        values = row
        # print values[u'代码']
        try:
            # conn=MySQLdb.connect(host='203.195.179.183',user='cdb_outerroot',passwd='24203cjy',port=8295,db='test',charset='utf8')
            conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='24203cjy', port=3306, db='test',
                                   charset='utf8')
            cur = conn.cursor()
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
            value = [10,
                     values[u'代码'][0:2],
                     values[u'代码'][2:8],
                     values[u'    名称'],
                     '公司', '行业代码A', '行业名称A',
                     '20' + time.strftime("%y%m%d"),
                     '20' + time.strftime("%y%m%d"),
                     1,  #发布价格
                     'RMB',  #货币
                     10,  #数量
                     '区域',  # 区域
                     '1']  #状态
            # print value
            sql = '''INSERT INTO STKPRODUCT (CUNTRYCD, MARKETTPPE, STKCODE , STKNAME ,
                            CONAME, INDCODE , INDNAME , ESTBDATE, LISTDATE, IPOPRC,
                            IPOCUR  , NSHRIPO , SCTCODE , STATCO )
                    VALUE
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            cur.execute('delete from STKPRODUCT where STKCODE=\''+values[u'代码'][2:8]+'\'')
            cur.execute(sql, value)
            status=0
            # 插入交易表  values[1].decode("gbk").encode("utf-8"),
            if values[u'现价'] == '--':
              status=1
            else:
              status=2
            stockCode = values[u'代码']
            value=[values[u'代码'][2:8],   # STKCODE      varchar(12)
                    values[u'代码'][0:2],      # MARKETTYPE   varchar(2) '市场类型'
                    skDate,  # TRDDATE      int(8) NOT NULL COMMENT '交易日期' ,
                    values[u'昨收'],       # PRECLSPRC    varchar(255)  '昨日收盘价' ,
                    iif(status == 1,0,values[u'开盘']),  # OPNPRC DECIMAL (4, 4) NULL DEFAULT NULL COMMENT '日开盘价',
                    iif(status == 1,0,values[u'最高']),       # HIPRC DECIMAL (4, 4) NULL DEFAULT NULL COMMENT '日最高价',
                    iif(status == 1,0,values[u'最低']),         # LOPRC        decimal(4,4) NULL DEFAULT NULL COMMENT '日最低价' ,
                    iif(status == 1,0,values[u'现价']),    # CLSPRC       decimal(4,4) NULL DEFAULT NULL COMMENT '日收盘价' ,
                    iif(status == 1,0,values[u'涨跌']),    # ADV DECIMAL (4, 4) NULL DEFAULT NULL COMMENT '涨跌值',
                    iif(status == 1,0,values[u'涨幅%']),    # ADR          decimal(4,4) NULL DEFAULT NULL COMMENT '涨跌率 * 100' ,
                    iif(values[u'总手'] == '--',0,values[u'总手']),    # VOL DECIMAL (20, 0) NULL DEFAULT NULL COMMENT '日个股交易股数 成交量',
                    values[u'总金额'],    # AMOUNT       varchar(20) '日成交额' ,
                    iif(values[u'流通市值'] == '--',0,values[u'流通市值']),    # CAPITAL VARCHAR (20) '流通市值',
                    iif(values[u'总市值'] == '--',0,values[u'总市值']),    # CAPTOTAL     varchar(20) '总市值' ,
                    iif(values[u'市盈(动)'] == '--',0,values[u'市盈(动)']),    # PE DECIMAL (4, 2) NULL DEFAULT NULL COMMENT '市盈率',
                    iif(values[u'市净率'] == '--',0,values[u'市净率']),    #  PB           decimal(4,2) NULL DEFAULT NULL COMMENT '市净率' ,
                    iif(values[u'外盘'] == '--',0,values[u'外盘']),    # BUYVOL       decimal(10,0) NULL DEFAULT NULL COMMENT '外盘量' ,
                    iif(values[u'内盘'] == '--',0,values[u'内盘']),    # SELLVOL      decimal(10,0) NULL DEFAULT NULL COMMENT '内盘量' ,
                    status   # TRDSTA       varchar(2)  '交易状态
                ]
            sql = '''INSERT INTO STKTRADE (STKCODE, MARKETTYPE, TRDDATE, PRECLSPRC,
                            OPNPRC, HIPRC, LOPRC, CLSPRC, ADV, ADR, VOL, AMOUNT,
                            CAPITAL, CAPTOTAL, PE, PB, BUYVOL, SELLVOL, TRDSTA )
                        VALUE
                          (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )'''

            cur.execute('delete from STKTRADE where STKCODE=\''+values[u'代码'][2:8]+'\''+' and TRDDATE='+skDate)
            cur.execute (sql,value)
            conn.commit()
            cur.close()
            conn.close()


        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    print "执行成功 共" +'%d' %len(tables) +'条 现在执行第 '+ '%d' %rn +'条！'