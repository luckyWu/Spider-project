# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request
from scrapy import Request
from lxml import etree
from bs4 import BeautifulSoup
import requests

from anjuKe.items import AnjukeItem

n = 0



class AjkSpider(scrapy.Spider):
    name = 'ajk'
    allowed_domains = ['*']
    start_urls = ['http://sz.zu.anjuke.com/']

    citys_url = 'https://www.anjuke.com/sy-city.html'

    url = 'https://sz.zu.anjuke.com/?from=navigation'

    def start_requests(self):
        yield Request(self.citys_url, dont_filter=True, callback=self.parse)

    def parse(self, response):

        global n
        print(response.status,'-------------status')
        res = (response.text)
        be = BeautifulSoup(res)
        print(be.title.string)
        # print(res)
        html = etree.HTML(res)
        cons = html.xpath('//div[@class="letter_city"]/ul//li')
        # print(cons)
        for con in cons[:]:
            citys = con.xpath('.//div[@class="city_list"]//a')
            for every_city in citys[:]:
                href = every_city.xpath('./@href')
                city = every_city.xpath('./text()')
                if href:
                    yield Request(href[0], dont_filter=True, callback=self.parse_city)
                print(n,city, href)
                # n  += 1

    def parse_city(self, response):
        global n
        print(response.status)
        res = ( response.text)
        html = etree.HTML(res)
        con = html.xpath('//li[@class="li_single li_itemsnew li_unselected"]//a[@class="a_navnew"]/@href')
        if con:
            print('-----------',con,'----------------')
            yield Request(con[2], dont_filter=True, callback=self.parse_zu)

    def parse_zu(self, response):
        global n
        print(response.status)
        res = ( response.text)
        html = etree.HTML(res)
        bs = BeautifulSoup(res, 'lxml')
        b4 = bs.title.string
        # print(b4)
        # print('------into------')
        # l = re.findall(r'<a href="(.*?)" class="next-page next-link">下一页',res)
        # print('--------------l-------------',l)
        cons = html.xpath('//div[@class="zu-itemmod  "]')#div[@class="item-mod "]')
        next = html.xpath('//a[@class="aNxt"]/@href')
        # print('next',cons,'<-------------next------------------->')
        for con in cons[:]:
            print('into------------')
            img_url = con.xpath('./a/img/@src')
            title = con.xpath('./div[@class="zu-info"]/h3/a/text()')
            info = con.xpath('./div[@class="zu-info"]/p//text()')
            addr = con.xpath('./div[@class="zu-info"]/address[@class="details-item"]//text()')
            price = con.xpath('./div[@class="zu-side"]/p/strong/text()')
            print(n, title, info,addr, price, img_url)
            item = AnjukeItem()
            item['img_url'] = img_url[0] if img_url else ''
            item['title'] = title[0] if title else ''
            item['info'] = info[0] if info else ''
            item['price'] = price[0] if price else ''
            item['addr'] = addr
            yield item

            n += 1
        if next:
            yield Request(next[0], dont_filter=True, callback=self.parse_zu)


