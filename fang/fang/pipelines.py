# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from fang.items import FangItem, urlItem


class FangPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def _url_item(self, item):
        self.db[item.table_name].insert(dict(item))
        return item

    def _Be_item(self, item):
        self.db[item.table_name].insert(dict(item))
        return item

    def process_item(self, item, spider):
        if isinstance(item,FangItem):
            return self._Be_item(item)
        elif isinstance(item,urlItem):
            return self._url_item(item)
        else:
            return item
