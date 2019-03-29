# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class BeikeItem(scrapy.Item):
    table_name = 'beike'
    id = Field()
    title = Field()
    jb_info = Field()
    loupan_js = Field()
    loupan_guihua = Field()
    sm_zige = Field()
    peitao_info = Field()

class urlItem(scrapy.Item):
    table_name = 'beikeurl'
    id = Field()
    img_url = Field()
    title = Field()

class ershouItem(scrapy.Item):
    table_name = 'ershou'
    title = Field()
    price = Field()
    img = Field()
    tots = Field()