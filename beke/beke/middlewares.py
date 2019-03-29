# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from scrapy import signals

from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError

cc =0
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
    if cc > 60:
        print('--------次数已经到底-----------')
        return None
    print('开始获取代理IP------------------------------------------!')
    try:
        s = requests.get(url='http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=02ea7237a8ee48f19df3b4b035e428cd&count=1&expiryDate=0&format=1&newLine=3')
        res = json.loads(s.text)
        ips = res['msg'][0]
        ip1 = 'http://'+ips['ip']+':'+ips['port']
        print('成功获取代理IP',ip1)
        return str(ip1)
    except:
        time.sleep(10)
        test_ip()


# ip = test_ip()
gip = get_ip()


class BeikeDownloaderMiddleware(object):
    def __init__(self, user_agent):
        global gip

        self.ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                          ConnectionRefusedError, ConnectionDone, ConnectError,
                          ConnectionLost, TCPTimedOutError, ResponseFailed,
                          IOError, TunnelError)
        self.user_agent = user_agent
        self.n = 0
        self.ip = gip

    def get_ip(self):
        try:
            s = requests.get('http://129.28.109.42:5000/random')
            k = 'http://' + s.text
            return k
        except:
            time.sleep(10)
            self.get_ip()
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # global ip
        # self.n += 1
        # if self.n > 60:
        #     print('-------------主动换ip---------------------')
        #     ip = get_ip()
        #     self.n = 0
        request.meta['proxy'] = self.ip
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
        # ua = UserAgent(verify_ssl=False)
        # print(ua.random) # 使用后效果不好1000就停了
        # request.headers.setdefault("User-Agent", ua.random)
        request.meta['download_timeout'] = 25
        print('----------当前代理IP-->',self.ip)

    def process_response(self, request, response, spider):
        # global ip
        print(response.status, '状态！！！！！！！！！！')
        if response.status != 200:

           text = response.text
           if response.status == 503:
               print('--------------503-------------------')
               print(response.text)
               time.sleep(3)
               return request
           # ip = test_ip()
           self.ip = self.get_ip()
           print(response.status,'-----------------process_reponse---')
           request.meta['proxy'] = self.ip
           # logging.warning(f'{response.status}and---{response.url}----andand{text}')
           time.sleep(4)
           return request
        return response

    def process_exception(self, request, exception, spider):
        # global ip
        if isinstance(exception, self.ALL_EXCEPTIONS[-1]):
            print('503-----------')
            time.sleep(2)
            pass
        elif isinstance(exception, self.ALL_EXCEPTIONS):
            # 在日志中打印异常类型

            print('Got exception: %s' % (exception))

            print('----------------error-------------',request.url)
            # ip = test_ip()
            self.ip = self.get_ip()
            print('ip is genghuan-------->',self.ip)
            time.sleep(10)
            request.meta['proxy'] = self.ip
            return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
