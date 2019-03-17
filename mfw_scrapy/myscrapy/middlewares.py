# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from scrapy import log

from threading import Thread

# from scrapy import signals
import requests,json
from collections import deque

import time, re

from fake_useragent import UserAgent

global curent_ip, q
q = deque(maxlen=500)

def getip():
    time.sleep(12)
    url='http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=98c6acfa913841469559968991e79315&count=5&expiryDate=0&format=2&newLine=2'
    if len(q) < 3:
        res = requests.get(url)
        ips = (res.content.decode('utf-8'))
        print(ips)
        if re.match(r'\d+\.', ips):
            # q.append(k)
            ip = ips.split('\r\n')
            for i in ip[:5]:
                proxy = 'http://'+i
                q.append(proxy)
# getip()


time.sleep(3)
# curent_ip = q.pop()
# print('ip已准备！！！！！！！！！！！！',curent_ip)
# print(1,curent_ip,q)
class MyscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyscrapyDownloaderMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # def __init__(self):
    #     self.curent_ip = q.pop()

    # @classmethod
    # def from_crawler(cls, crawler):
    #     # This method is used by Scrapy to create your spiders.
    #
    #     crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    #     return s

    def process_request(self, request, spider):
        # pass
        # request.meta['proxy'] = a
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # print(curent_ip)
        # if not re.match(r'\d+\.',curent_ip):
        #     time.sleep(8)
        #     getip()
        # curent_ip = q.pop()
        # ua = UserAgent()
        # request.headers.setdefault("User-Agent", ua.random)
        # request.cookies = ''
        # request.meta['proxy'] = curent_ip
        # time.sleep(2)
        pass

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # return response
        # print(response.status)
        # if response.status in [403, 301]:
        #     try:
        #         time.sleep(10)
        #         getip()
        #         curent_ip = q.pop()
        #         print('try_ip')
        #         request.meta['proxy'] = curent_ip
        #         print(request.meta)
        #         return request
        #     except Exception:
        #         print('process_response1--------------------------')
        #         return response
        #
        # else:
        #     print('process_response2--------------------------')
        if response.status != 200:
            log.msg("This is a warning{n}".format(response.status), level=log.WARING)
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
        # self.logger = logging.getLogger(__name__)
        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        # getip()
        # self.logger.debug('exception error -------------------------')
        # time.sleep(12)
        # curent_ip = q.pop()
        # print(curent_ip)
        # request.meta['proxy'] = curent_ip
        # request.cookies = ''
        # return request
        log.msg("This is a warning{n}".format(exception), level=log.WARING)
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
if __name__ == "__main__":
    print("")