# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy import Request,Spider
from lxml import etree

from digikey.items import DigikeyItem

n =1
class DigikeyComSpider(Spider):
    name = 'digikey_com'
    allowed_domains = ['www.digikey.com']
    start_urls = ['http://www.digikey.com/']
    f_url = 'https://www.digikey.com/products/en'

    def start_requests(self):
        yield Request(self.f_url, dont_filter=True, callback=self.parse)

    def parse(self, response):
        """解析每个地点"""

        print(response.status)
        if response.status == 200:
            s = etree.HTML(response.text)
            # print(res.text)
            con = s.xpath('//div[@id="productIndexList" and contains(@class,"catfilters")]')
            print(con)
            if con:
                uls = con[0].xpath('.//ul[@class="catfiltersub"]')
                # print(uls)
                for ul in uls[:]:
                    lis = ul.xpath('./li')
                    # print(lis)
                    for li in lis[:]:
                        href = li.xpath('./a/@href')
                        if href:
                            href1 = 'https://www.digikey.com' + href[0]
                            print(href1)
                            yield Request(href1, dont_filter=True, callback=self.parse_data)
                            # pares_li(href1)
                    # title = li.xpath('./a/text()')
                    # print(href, title)
            else:
                # print(response.text)
                # print(f'------------{response.status}')
                # logging.warning(f"parse失败:{response.status}")
                print(response.text)


    def parse_data(self, response):
        """解析每个地点"""
        global n
        print(response.status)
        if response.status == 200:
            # if n==6:
            #     print(response.text)
            s = etree.HTML(response.text)
            cag = s.xpath('//h1[@class="breadcrumbs" and contains(@itemprop,"breadcrumb")]/a')
            if cag:
                cat = cag[1].xpath('string(.)')
                next_href = s.xpath('//a[@class="Next"]/@href')
                # print(n, next_href)
                cons = s.xpath('//table[@id="productTable" and contains(@class,"productTable")]/tbody/tr')
                for con in cons[:]:
                    tds = con.xpath('./td')[:]

                    doc_url = tds[1].xpath('string(./center)')
                    img_url = tds[2].xpath('./a/img/@src')[0] if tds[2].xpath('./a/img/@src') else ''
                    Digi_Key = tds[3].xpath('string(./a)').strip()
                    Manufacturer = tds[4].xpath('string(.)').strip()
                    Description = tds[5].xpath('string(.)').strip()
                    Accessory_Type = tds[12].xpath('string(.)').strip() if len(tds)>=12 else ''
                    item = DigikeyItem()
                    item['cat'] = cat
                    item['doc_url'] = doc_url
                    item['img_url'] = img_url
                    item['Digi_Key'] = Digi_Key
                    item['Manufacturer'] = Manufacturer
                    item['Description'] = Description
                    item['Accessory_Type'] = Accessory_Type
                    yield item
                    # td.xpath('string(.)').strip().replace('\r\n','')
                    # print(n, doc_url, img_url, Digi_Key, Manufacturer, Description,Accessory_Type)
                # tr = [td.xpath('string(.)').strip().replace('\r\n','') for td in con.xpath('./td')[4:]]
                # print(n, tr)
                n += 1
                if next_href:

                    nhref = 'https://www.digikey.com' + next_href[0]
                    print(nhref)
                    yield Request(nhref, dont_filter=True, callback=self.parse_data)

                else:
                    print(next_href,'next_href is not find !!!!!!!!!!!!')
                    print(response.url)
                    # logging.warning(f"parse_data失败:{response.status}")
            else:
                print('cag is not find !!!!!!!')


