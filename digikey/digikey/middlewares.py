# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
from bs4 import BeautifulSoup
from scrapy.exceptions import IgnoreRequest
import requests
import time
import lxml
from fake_useragent import UserAgent
from scrapy import signals
from uuid import uuid1
cc= 0
def get_ip():
    try:
        s = requests.get('http://129.28.109.42:5000/random')
        ip = 'http://' + s.text
        return ip
    except:
        time.sleep(10)
        get_ip()
def test_ip():
    global cc
    cc += 1
    if cc > 150:
        print('--------次数已经到底-----------')
        return None
    print('开始获取代理IP------------------------------------------!')
    try:
        s = requests.get(url='http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=02ea7237a8ee48f19df3b4b035e428cd&count=1&expiryDate=0&format=1&newLine=3')
        res = json.loads(s.text)
        ips = res['msg'][0]
        ip_my = 'http://'+ips['ip']+':'+ips['port']
        print('成功获取代理IP',ip_my)
        return str(ip_my)
    except:
        time.sleep(10)
        test_ip()

# ip = get_ip()
ip = get_ip()
# ip = test_ip()
# n = 1
class DigikeyDownloaderMiddleware(object):

    def __init__(self):
        # global n
        self.ran = time.time()#random.randint(0,10)
        self.cookie = {'i10c.eac23': str(self.ran)+str(uuid1()) }
        self.count = 0

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        global ip
        print('start!!!!')
        if self.count > 2:
            print('住洞换ip')
            ip=get_ip()
            self.count = 0
        self.count += 1
        request.cookies = self.cookie
        # ua = UserAgent(verify_ssl=False)
        # print(ua.random) # 使用后效果不好1000就停了
        # request.headers.setdefault("User-Agent", ua.random)
        request.meta['proxy'] = ip
        request.meta['download_timeout'] = 8
        print(ip,'this is proxy ip')
        # return None

    def process_response(self, request, response, spider):
        global ip
        # n += 1
        if response.status == 200:
            soup = BeautifulSoup(response.text,'lxml')
            cont = soup.body.string
            print(cont,'this is bs4 obj')

            if isinstance(cont, str) and 'HtmlStreaming.ReloadWithNoHtmlStreaming' in cont:
            # print(response.status,len(cont),'----------》')
            # if cont is None:
                # logging.warning(f"parse_data失败:{response.text}")
                time.sleep(3)
                ip = get_ip()
                # ip=test_ip()
                request.meta['proxy'] = ip
                return request
            return response
        elif response.status == 403:
            time.sleep(4)
            ip = get_ip()
            # ip=test_ip()
            request.meta['proxy'] = ip
            return request
        else:
            raise  IgnoreRequest


    def process_exception(self, request, exception, spider):
        global ip
        # request.meta['proxy'] = get_ip()
        # return request
        time.sleep(10)
        # ip = test_ip()
        ip = get_ip()
        logging.warning(f"parse失败:{exception}")
        print(ip,'准备换IP!!!!!!!!!!')
        # n += 1
        request.meta['proxy'] =ip
        request.cookies = self.cookie
        return request

        # ip = get_ip()
        # return None
    # ip = get_ip()


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
