# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AnjukeItem(Item):
    """创建名为anjuke的item"""
    table_name = 'anjuke'

    img_url = Field()
    title = Field()
    info = Field()
    addr = Field()
    price = Field()
