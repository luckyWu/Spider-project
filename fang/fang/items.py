# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class FangItem(scrapy.Item):
    table_name = 'xin_fang'

    id = Field()
    title = Field()
    jb_info = Field()
    xiaoshou_info = Field()
    zhoubian_sheshi = Field()
    gui_hua = Field()
class urlItem(scrapy.Item):
    table_name = 'url'
    id = Field()
    img_url = Field()
