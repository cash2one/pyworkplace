# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class productItem(Item):
    CUNTRYCD = Field()  # '国家代码    本数据库以10表示中国',
    STKCODE = Field()  # '证券代码',
    STKNAME = Field()  # '证券名称',
    CONAME = Field()  # '公司名称',
    INDCODE = Field()  # '行业代码A',
    INDNAME = Field()  # '行业名称A',
    NINDCOME = Field()  # '行业代码B',
    NINDNAME = Field()  # '行业名称B',
    ESTBDATE = Field()  # '公司成立日期',
    LISTDATE = Field()  # '上市日期',
    IPOPRC = Field()  # '发行价格',
    IPOCUR = Field()  # '发行货币 发行价格的计量货币   CNY=人民币元，HKD=港币，USD=美元',
    NSHRIPO = Field()  # '发行数量',
    SCTCODE = Field()  # '区域码 1=上海，2=深圳',
    STATCO = Field()  # '公司活动情况  A=正常交易，D＝终止上市，S=暂停上市， N=停牌',
    MARKETTPPE = Field()  # '市场类型    1=上海A，2=上海B，4=深圳A，8=深圳B, 16=创业板',


class tradeItem(Item):
    STKCODE = Field()  #
    TRDDATE = Field()  #
    OPNPRC = Field()  # '日开盘价',
    HIPRC = Field()  # '日最高价',
    LOPRC = Field()  # '日最低价',
    CLSPRC = Field()  # '日收盘价',
    ADV = Field()  # '涨跌值',
    ADR = Field()  # '涨跌率 * 100',
    DNSHRTRD = Field()  # '日个股交易股数 0=没有交易量',
    DNVALTRD = Field()  # 'DECIMAL 日个股交易金额 计量货币：人民币元。A股以人民币元计，上海B以美元计，深圳B以港币计，0=没有交易量',
    DSMVOSD = Field()  # '日个股流通市值 个股的流通股数与收盘价的乘积，A股以人民币元计，上海B股以美元计，深圳B股以港币计',
    DSMVTLL = Field()  # '日个股总市值  个股的发行总股数与收盘价的乘积，A股以人民币元计，上海B股以美元计，深圳B股以港币计',
    MARKETTYPE = Field()  # '市场类型    1=上海A，2=上海B，4=深圳A，8=深圳B, 16=创业板',
    TRDSTA = Field()  # '1' COMMENT '交易状态    1=正常交易，2=ST，3＝*ST，4＝S',