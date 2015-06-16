# -*- coding: utf-8 -*-

# Scrapy settings for dbmoive project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dbmoive'

SPIDER_MODULES = ['dbmoive.spiders']
NEWSPIDER_MODULE = 'dbmoive.spiders'
ITEM_PIPELINES = ['dbmoive.pipelines.DoubanmoivePipeline']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dbmoive (+http://www.yourdomain.com)'
