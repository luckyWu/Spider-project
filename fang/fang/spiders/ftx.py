# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request
from lxml import etree
from bs4 import BeautifulSoup
# from beke.items import urlItem, BeikeItem
from fang.items import FangItem, urlItem


class FtxSpider(scrapy.Spider):
    name = 'ftx'
    allowed_domains = ['*']
    start_urls = ['http://fang.com/']

    url = 'https://www.fang.com/SoufunFamily.htm?ctm=1.bj.xf_search.head.29'

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
            t2 = html.xpath('//table[@class="table01"]')[1]
            cons = t2.xpath('.//tr')
            # print(cons)
            for con in cons[:]:
                citys = con.xpath('./td[last()]/a')
                for every_citys in citys[:]:
                    title = every_citys.xpath('./text()')[0]
                    href = every_citys.xpath('./@href')[0]
                    print(title,href)
                    if not href.startswith('https://world'):
                        yield Request(href, dont_filter=True, callback=self.xuanze)

    def xuanze(self,response):
        print(response.status)
        if response.status == 200:
            html = etree.HTML(response.text)
            t2 = html.xpath('//div[@class="newnav20141104nr"]')
            cons = t2[0].xpath('./div[@class="s5" and contains(@track-id,"newhouse")]//a')
            # print(t2)
            s = cons[0].xpath('./@href')[0]
            yield Request(s, dont_filter=True, callback=self.loupan)

    def loupan(self,response):
        '''
        每个城市所有楼盘
        :param response:
        :return:
        '''
        print(response.status)
        if response.status == 200:
            base_url = response.url
            html = etree.HTML(response.text)
            lous = html.xpath('//div[@class="nl_con clearfix" and contains(@id,"newhouse_loupai_list")]/ul/li')
            if lous:
                for lou in lous:
                    img_url = lou.xpath('./div[@class="clearfix"]/div[@class="nlc_img"]/a/img/@src')
                    if (img_url and len(img_url)>=2):
                        i_url = img_url[1]
                    else:
                        i_url = ''

                    t_obj = lou.xpath('./div[@class="clearfix"]/div[@class="nlc_details"]//a')
                    if t_obj:
                        item = urlItem()
                        href = t_obj[0].xpath('./@href')
                        title = t_obj[0].xpath('./text()')
                        print(title,'--------------this is title')
                        if title:
                            item['id'] = title[0].strip().replace('\t','').replace('\n','')
                            item['img_url'] = i_url
                            yield item

                        if href:
                            in_href = 'https:' + href[0]
                            yield Request(in_href, dont_filter=True, callback=self.base_parse)
                    else:
                        print(t_obj)

                if '/b9' not in base_url:
                    n_href = re.sub('house/s','house/s/b92',base_url)
                    yield Request(n_href, dont_filter=True, callback=self.loupan)
                else:
                    obj = re.search('/s/b9(\d+)/',base_url)
                    if obj:
                        temp = int(obj.group(1)) + 1
                        tt = '/s/b9' + str(temp) + '/'
                        n1_href = re.sub('/s/b9(\d+)/',tt,base_url)
                        yield Request(n1_href, dont_filter=True, callback=self.loupan)

    def base_parse(self,response):
        '''
        楼盘基本信息页
        :param response:
        :return:
        '''
        print(response.status)
        if response.status == 200:
            html = etree.HTML(response.text)
            detail_page = html.xpath('//div[@class="fl more"]/p/a/@href')
            if detail_page:
                detail_url = 'https:' + detail_page[0]
                yield Request(detail_url, dont_filter=True, callback=self.detail_parse)

    def detail_parse(self,response):
        """
        新楼详情页
        :param response:
        :return:
        """
        print(response.status)
        if response.status == 200:
            html = etree.HTML(response.text)
            detail_page = html.xpath('//div[@class="main-left"]//div[@class="main-item"]')

            dtitle = html.xpath('//div[@class="lpbt tf jq_nav"]/h1/a/text()')
            soup = BeautifulSoup(response.text, 'lxml')
            item = FangItem()
            if soup:
                item['title'] = soup.title.string
            else:
                item['title'] = ''
            if dtitle:
                item['id'] = dtitle[0]
            else:
                item['id'] = ''
            if detail_page:
                # print(detail_page)
                item['jb_info']= (detail_page[0].xpath('string(.)').strip().replace('\t','').replace('\n', ''))
                item['xiaoshou_info'] = (detail_page[1].xpath('string(.)').strip().replace('\t', '').replace('\n', ''))
                item['zhoubian_sheshi'] = (detail_page[2].xpath('string(.)').strip().replace('\t', '').replace('\n', ''))
                item['gui_hua']= (detail_page[3].xpath('string(.)').strip().replace('\t','').replace('\n', ''))
            # print(item)
            yield item

