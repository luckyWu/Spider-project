# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request
from lxml import etree
from bs4 import BeautifulSoup

from beke.items import ershouItem


class ErshouSpider(scrapy.Spider):
    name = 'ershou'
    allowed_domains = ['*']

    start_urls = ['http://www.ke.com/']

    url = 'https://www.ke.com/city/'
    def __init__(self):
        self.g = -3

    def start_requests(self):
        yield Request(self.url, dont_filter=True, callback=self.parse)

    def parse(self, response):
        """
        获取所有城市
        :param response:
        :return:
        """
        global n
        print(response.status, '-------------status')
        # print(response.text)
        if response.status == 200:
            html = etree.HTML(response.text)
            cons = html.xpath('//ul[@class="city_list_ul"]/li')
            # print(cons)
            for con in cons[:]:
                citys = con.xpath('.//div[@class="city_list"]/div/ul')
                for every_citys in citys[:]:
                    cs = every_citys.xpath('./li')
                    for city in cs[:]:
                        city_obj = city.xpath('./a/@href')
                        tit = city.xpath('string(.)')

                        if city_obj and not city_obj[0].startswith('//i'):
                            print('城市=', tit, '连接=', city_obj[0])
                            i_href = 'https:' + city_obj[0]
                            yield Request(i_href, dont_filter=True, callback=self.parse_souye)


    def parse_souye(self, response):
        """
        首页选择
        :param response:
        :return:
        """
        print(response.status, '-------------souye')
        # print(response.text)
        if response.status == 200:
            html = etree.HTML(response.text)
            print(html.xpath('//div[@class="nav typeUserInfo"]'))
            cons = html.xpath('//div[@class="nav typeUserInfo"]//ul/li')
            if (cons):
                print(response.url,'-----------------------')
                i_t = cons[0].xpath('./a/text()')
                hf = cons[0].xpath('./a/@href')
                if i_t and i_t[0] == '二手房':
                    yield Request(hf[0], dont_filter=True, callback=self.parse_citys)

    def parse_citys(self, response):
        """
        每个地点所有子地点
        :param response:
        :return:
        """
        print(response.status, '-------------fangs')
        res = (response.text)
        if response.status == 200:
            base_url = response.url
            html = etree.HTML(response.text)
            cits = html.xpath('//div[@class="m-filter" and contains(@data-component,"C_filter")]//div[@data-role="ershoufang"]/div/a')
            for cit in cits[:]:
                ahf = cit.xpath('./@href')
                atx = cit.xpath('./text()')
                print(ahf,atx)
                if ahf:
                    nn_href = re.sub(r'/ershoufang/',ahf[0],base_url)
                    yield Request(nn_href, dont_filter=True, callback=self.parse_fangs)

    def parse_fangs(self, response):
        """
        每个地点所有房屋
        :param response:
        :return:
        """
        print(response.status, '-------------fangs')
        res = (response.text)
        if response.status == 200:
            base_url = response.url
            soup = BeautifulSoup(response.text, 'lxml')
            t = soup.title.string
            res = re.search(r'第(\d+)页',t)
            url_num= re.search(r'/pg(\d+)/',base_url)
            if url_num:
                base_num = url_num.group(1)
            else:
                base_num = -1

            print(t)
            html = etree.HTML(response.text)
            fangs = html.xpath('//div[@data-component="list"]/ul//li')
            print(len(fangs))
            n = 1
            pri_tit = self.g
            for fang in fangs[:1]:

                img = fang.xpath('./a/img[@class="lj-lazy"]/@src')
                title = fang.xpath('div[@class="info clear"]/div[@class="title"]/a/text()')
                if n == 1:
                    # 比较上一页的title，相同说明结束
                    if self.g == -3 or self.g != title[0]:
                        if title:
                            self.g = title[0]
                    else:
                        print('over!!!!!!!!')
                        return
                n += 1
                det_href = fang.xpath('div[@class="info clear"]/div[@class="title"]/a/@href')
                if det_href:
                    yield Request(det_href[0], dont_filter=True, callback=self.parse_detail)


                if res:
                    num = int(res.group(1)) + 1
                    n_href = re.sub(r'/pg(\d+)/','/pg{n}/'.format(n=num),base_url)
                    yield Request(n_href, dont_filter=True, callback=self.parse_fangs)
                else:
                    print('还没有第几页呢@@@@@@@@@')
                    num = 2
                    n_href = base_url + 'pg2/'
                    yield Request(n_href, dont_filter=True, callback=self.parse_fangs)


    def parse_detail(self, response):
        """
        房屋详细信息
        :param response:
        :return:
        """
        print(response.status, '-------------detail')
        # print(response.text)
        if response.status == 200:
            html = etree.HTML(response.text)
            title = html.xpath('//div[@class="title-wrapper" and contains(@log-mod,"detail_header")]/div[@class="content"]/div[@class="title"]/h1/text()')
            contents = html.xpath('//div[@class="overview"]//div[@class="content"]')
            imgs = html.xpath('//div[@class="overview"]//ul[@class="smallpic"]/li[1]/img/@src')
            if contents:
                item = ershouItem()
                tots = contents[0].xpath('string(.)').strip().replace('\n','')
                price = contents[0].xpath('./div[@class="price "]/span[@class="total"]/text()')
                item['title'] = title[0].strip().replace('\n','') if title is not None else ''
                item['price'] = price[0] if price is not None else ''
                item['img'] = imgs[0] if imgs is not None else ''
                item['tots'] = tots
                yield item



                # print(cons)


            # i_t = cons[0].xpath('./a/text()')
            # hf = cons[0].xpath('./a/@href')
            # if i_t and i_t[0] == '二手房':
            #     yield Request(hf[0], dont_filter=True, callback=self.parse_fangs)
