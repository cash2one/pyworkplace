# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class DbbookItem(Item):
      title =Field()
      link = Field()


class DmozItem(Item):
      title = Field()
      link = Field()
      desc = Field()