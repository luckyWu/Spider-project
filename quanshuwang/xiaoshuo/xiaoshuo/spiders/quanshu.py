# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request
from lxml import etree
import time
from xiaoshuo.items import XiaoshuoItem

class QuanshuSpider(Spider):
    name = 'quanshu'
    allowed_domains = ['quanshuwang.com']
    start_urls = ['http://quanshuwang.com/']
    list_url = 'http://www.quanshuwang.com/shuku/'

    def start_requests(self):
        yield Request(self.list_url, dont_filter=True, callback=self.parse)

    def parse(self, response):
        """小说列表解析"""
        if response.status == 200:
            results =  response.text
            html = etree.HTML(results)
            if html:
                # 获取每本小说链接
                next = html.xpath('//a[@class ="next"]/@href')
                target = html.xpath('//div[@class="contents yd-rank-content yd-book-content"]')[0]
                lis = target.xpath('.//div[@class="yd-book-item yd-book-item-pull-left"]')
                for li in lis[:]:
                    href = li.xpath('./a/@href')
                    # auth = li.xpath('.//dl[@class="dl-horizontal-inline"]//p/text()')[0]
                    if href:
                        yield Request(href[0], dont_filter=True, callback=self.brief_parse)
                # 下一页
                if next:
                    yield Request(next[0], self.parse)

    def brief_parse(self, response):
        """小说简述解析"""
        if response.status == 200:
            results =  response.text
            html = etree.HTML(results)
            if html:
                chapter_href = html.xpath('//div[@class="b-oper"]/a/@href')
                if chapter_href:
                    yield Request(chapter_href[0],dont_filter=True,  callback=self.chapter_parse)

    def chapter_parse(self, response):
        """章节列表"""
        if response.status == 200:
            results =  response.text
            html = etree.HTML(results)
            if html:
                # 获取每一章节链接
                chapters = html.xpath('//div[@class="clearfix dirconone"]//li')
                if chapters:
                    for chapter in chapters[:]:
                        chapter_name = chapter.xpath('./a/text()')
                        content_href = chapter.xpath('./a/@href')
                        if content_href:
                            yield Request(content_href[0],dont_filter=True, callback=self.content_parse)


    def content_parse(self, response):
        """每章内容"""
        if response.status == 200:
            html = etree.HTML(response.text)
            if html:
                title = html.xpath('//em[@class="l"]/text()')
                page = html.xpath('//strong[@class ="l jieqi_title"]/text()')
                content = html.xpath('//div[contains(@class, "mainContenr") and @id="content"]/text()')

                item = XiaoshuoItem()
                item['title'] = title[0] if title else ''
                item['page'] = page[0] if page else ''
                item['content'] = content
                yield item




