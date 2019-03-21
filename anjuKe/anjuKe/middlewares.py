# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import requests
from fake_useragent import UserAgent
from scrapy import signals
def get_ip():
    s = requests.get('http://129.28.109.42:5000/random')
    ip = 'http://' + s.text
    return ip


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxies'] = get_ip()

