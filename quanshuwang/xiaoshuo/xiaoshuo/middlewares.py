# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
from requests.exceptions import ConnectionError
from scrapy.exceptions import IgnoreRequest
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import hashlib
import json
import logging
import random
import time
from scrapy import signals
from fake_useragent import UserAgent
import requests, re
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError

def get_ip():
    s = requests.get('http://129.28.109.42:5000/random')
    if s.status_code== 200:
        ip = 'http://' + s.text
        return ip
    return None
def ran():
    s = random.randint(1,9999999999999999)
    return str(s)

def get_cookie():
    # c = {'security_session_verify':ran(),
    # 'jieqiVisitInfo':ran()}
    # return c
    url = 'http://127.0.0.1:8000/random'
    s = requests.get(url)

    if s.status_code == 200:
        return json.loads(s.text)
    else:
        return {}


def md5_key(arg):
    hash = hashlib.md5()
    hash.update(arg)
    return hash.hexdigest()


class XiaoshuoDownloaderMiddleware(object):

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """设置代理ip和cookie"""
        ua = UserAgent()
        request.headers.setdefault("User-Agent", ua.random)
        # request.meta['proxy'] =  get_ip()
        cookie = get_cookie()
        if cookie:
            request.cookies = cookie

    def process_response(self, request, response, spider):
        if response.status in [403]:
            try:
                request.cookies = get_cookie()
                print('403---------------------')
                # request.meta['proxy'] = get_ip()
                return request
            except Exception:
                raise IgnoreRequest
        else:
            return response


    def process_exception(self, request, exception, spider):

        # if isinstance(exception, self.ALL_EXCEPTIONS):
        #     print(request.meta)
        #     print(request.cookies)
        #     print('Got exception---------: %s' % (exception))
            # retries = request.meta.get('retry_times', 0) + 1
            # request.meta['retry_times'] = retries
        # time.sleep(10)
        # request.cookies = get_cookie()
        # return request
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
