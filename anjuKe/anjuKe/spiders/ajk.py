# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request
from scrapy import Request
from lxml import etree
from bs4 import BeautifulSoup
import requests

from anjuKe.items import AnjukeItem


class AjkSpider(scrapy.Spider):
    name = 'ajk'
    allowed_domains = ['*']
    citys_url = 'https://www.anjuke.com/sy-city.html'

    def start_requests(self):
        yield Request(self.citys_url, dont_filter=True, callback=self.parse)

    def parse(self, response):
        """解析每个地点"""

        # print(response.status,'-------------status')
        res = (response.text)
        html = etree.HTML(res)
        cons = html.xpath('//div[@class="letter_city"]/ul//li')

        # 获取每一个地点的链接
        for con in cons[:]:
            citys = con.xpath('.//div[@class="city_list"]//a')
            for every_city in citys[:]:
                href = every_city.xpath('./@href')
                city = every_city.xpath('./text()')
                if href:
                    yield Request(href[0], dont_filter=True, callback=self.parse_city)


    def parse_city(self, response):
        """获取租房的链接"""
        # print(response.status)
        res = ( response.text)
        html = etree.HTML(res)
        con = html.xpath('//li[@class="li_single li_itemsnew li_unselected"]//a[@class="a_navnew"]/@href')
        if con:
            yield Request(con[2], dont_filter=True, callback=self.parse_zu)

    def parse_zu(self, response):
        """解析租房信息"""

        print(response.status)
        res = ( response.text)
        html = etree.HTML(res)
        # bs = BeautifulSoup(res, 'lxml')
        # b4 = bs.title.string
        # print(b4)
        cons = html.xpath('//div[@class="zu-itemmod  "]')
        next = html.xpath('//a[@class="aNxt"]/@href') # 下一页链接

        for con in cons[:]:
            print('into------------')
            img_url = con.xpath('./a/img/@src')
            title = con.xpath('./div[@class="zu-info"]/h3/a/text()')
            info = con.xpath('./div[@class="zu-info"]/p//text()')
            addr = con.xpath('./div[@class="zu-info"]/address[@class="details-item"]//text()')
            price = con.xpath('./div[@class="zu-side"]/p/strong/text()')

            item = AnjukeItem()
            item['img_url'] = img_url[0] if img_url else ''
            item['title'] = title[0] if title else ''
            item['info'] = info[0] if info else ''
            item['price'] = price[0] if price else ''
            item['addr'] = addr
            yield item

        if next:
            yield Request(next[0], dont_filter=True, callback=self.parse_zu)


