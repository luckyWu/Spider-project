# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re


class MongoPipeline(object):
    collection_name = 'xiaoshuo2'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # print(self.db,'====================================')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        page = item['page']
        fpage = page
        fcontent = item['content']
        # 去格式
        content = re.sub(r'[\'\\r\\n,|\\xa0|\[|\]](\\xa0){0,4}', '', str(fcontent))
        if fpage:
            item['page'] = fpage
            item['content'] = content
            self.db[self.collection_name].insert(dict(item))#update({'url_token': item['url_token']}, dict(item), True)
        return item

