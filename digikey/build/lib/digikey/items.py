# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class DigikeyItem(scrapy.Item):
    table_name = 'digi1'
    cat = Field()
    doc_url = Field()
    img_url = Field()
    Digi_Key = Field()
    Manufacturer = Field()
    Description = Field()
    Accessory_Type = Field()
