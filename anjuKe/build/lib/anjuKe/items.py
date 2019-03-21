# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AnjukeItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'anjuke'
    img_url = Field()
    title = Field()
    info = Field()
    addr = Field()
    price = Field()
