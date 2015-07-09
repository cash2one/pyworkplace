# -*- coding: utf-8 -*-

# Scrapy settings for dbstock project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dbstock'

SPIDER_MODULES = ['dbstock.spiders']
NEWSPIDER_MODULE = 'dbstock.spiders'
ITEM_PIPELINES = ['dbstock.pipelines.MySQLStorePipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dbstock (+http://www.yourdomain.com)'
