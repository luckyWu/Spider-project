# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from myscrapy.db import get_con, get_cursor, insert

db = get_con()
cursor = get_cursor(db)



class MyscrapyPipeline(object):

    def process_item(self, item, spider):
        """写入数据库"""
        # if item['title']:
        insert(db, cursor, item)
        # else:
        #     pass
        return item


if __name__ =="__main__":
    item = {"title":""}
    print(list(item.values()))

    if bool(item):
        print("ok")