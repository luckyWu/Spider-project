# -*- coding: utf-8 -*-
# import scrapy
import json
import logging

import time
from lxml import etree
import re
from scrapy import Spider, Request
from scrapy import FormRequest
from myscrapy.items import MyscrapyItem
import random

ALL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyz'

def random_sn():
    """生成随机字符串"""

    s = ''
    chars_len = len(ALL_CHARS)
    for _ in range(10):
        index = random.randrange(chars_len)
        s += (ALL_CHARS[index])
    return s

def random_ts():
    """生成随机时间戳"""
    str = '0123456789'
    s = ['155']
    k = random.choice(s) + ''.join(random.choice(str) for i in range(10))
    return k

class FootballSpider(Spider):
    """解析网页"""

    name = 'football'
    allowed_domains = ['mafengwo.cn']
    start_urls = ['http://mafengwo.cn/']
    every_month_url = 'http://www.mafengwo.cn/mdd/base/filter/getlist'
    travel_url = 'http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist'
    base_month = 113
    params = {
        'mddid': '10189',
        'pageid': 'mdd_index',
        'sort': '1',
        'cost': '0',
        'days': '0',
        'month': '0',
        'tagid': '0',
        'page':'1',
        '_ts': random_ts(),
        '_sn': random_sn(),
    }
    month_params = {
        'tag[]': '113',
        'page': '1'
    }

    def start_requests(self):
        for month in range(0, 13):
            # 构建请求参数
            tag = 113 + month * 3
            month_num_params = self.month_params
            month_num_params['tag[]'] = str(tag)
            yield FormRequest(self.every_month_url, callback=self.parse, formdata=month_num_params)

    def parse(self, response):
        """解析每一页的每一个地点"""

        if response.status == 200 :
            res = json.loads(response.text)
            s = res.get('list', 0)

            if s:
                page_month = res.get('page', 0)
                obj = re.compile(r'<a rel="nofollow" data-page="(\d+)" href') # 提取下一页的请求参数
                obj1 = re.search(obj, page_month)
                html = etree.HTML(s)
                lis = html.xpath('//li[@class="item"]')
                for li in lis[:]:
                    href = li.xpath('./div[@class="img"]/a/@href')[0]
                    print(href,'show href--------')
                    mdds = href.split('/')[-1]
                    mdd = mdds.split('.')[0]
                    month_page_params = self.params
                    month_page_params['mddid'] = mdd
                    yield FormRequest(self.travel_url, callback=self.parse_travellist, formdata=month_page_params)
                if obj1:
                    month_page_next_params = self.params
                    month_page_next_params['page'] = obj1.group(1)
                    yield FormRequest(self.every_month_url, callback=self.parse,
                                      formdata=month_page_next_params)
        logging.warning(f"parse_list失败:{response.status}")



    def parse_travellist(self, response):
        """得到每一个地点的游记列表"""
        # print("into parse_travellist************************************")
        if response.status == 200 :
            print("enter")
            res = response.text
            content = json.loads(res)
            s = content.get('list', 0)
            page_info = content.get('page',0)
            #提取下一页的请求参数
            next = re.compile(r'<a class="pi pg-next" href="/yj/(\d+)/1-0-(\d+).html" title')
            next = re.search(next,page_info)

            if s:
                s = "<html>" + s + "</html>"
                html = etree.HTML(s)
                lis = html.xpath('//div[@class="tn-item clearfix"]')
                for li in lis[:]:
                    href1 = li.xpath('.//a[@class="title-link"]//@href')[0]
                    title = li.xpath('.//a[@class="title-link"]/text()')#('./div[@class="tn-wrapper"]/dl/dt/a/text()')
                    content = li.xpath('./div[@class="tn-wrapper"]/dl/dd/a/text()')
                    zan = li.xpath('./div[@class="tn-wrapper"]/div/span[@class="tn-ding"]/em/text()')
                    user_name = li.xpath('./div[@class="tn-wrapper"]/div/span[@class="tn-user"]/a/text()')
                    item = MyscrapyItem()
                    item['title'] = title[0] if title else ''
                    item['content'] = content[0] if content else ''
                    item['zan'] = zan[0] if zan else ''
                    item['user_name'] = user_name[0] if user_name else ''
                    yield item
                    # url = 'http://www.mafengwo.cn' + href1
                    # yield Request(url, callback=self.parse_detail, dont_filter=False)
                if next:
                    next_page = next.group(1) #获取参数midde的值
                    next_num = next.group(2) #获取参数page的值
                    every_page_params = self.params
                    every_page_params['mddid'] = next_page
                    every_page_params['page'] = next_num
                    yield FormRequest(self.travel_url, callback=self.parse_travellist,dont_filter=False, formdata=every_page_params)
            else:
                logging.warning(f"parse_travellist失败！：{response.status}")

    # def parse_detail(self, response):
    #     """每一个游记的详细内容"""
    #     print(response.text)