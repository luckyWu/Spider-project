# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request
from lxml import etree
from bs4 import BeautifulSoup
from beke.items import urlItem, BeikeItem

n = 0

class BkSpider(scrapy.Spider):
    name = 'bk'
    allowed_domains = ['www.ke.com']
    start_urls = ['http://www.ke.com/']

    url = 'https://www.ke.com/city/'

    def start_requests(self):
        yield Request(self.url, dont_filter=True, callback=self.parse)

    def parse(self, response):
        """
        获取所有城市
        :param response:
        :return:
        """
        global n
        print(response.status,'-------------status')
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
                            print('城市=', tit, '连接=', city_obj)
                            if 'fang'not in city_obj[0]:
                                temp = city_obj[0].split('.')
                                temp.insert(1,'fang')
                                temp = '.'.join(temp)

                            else:
                                temp = city_obj[0]
                            if temp.endswith('/'):
                                loupan_href = 'https:' + temp + 'loupan/'
                            else:
                                loupan_href = 'https:' + temp + '/loupan/'
                            print(loupan_href,'this is loupan------------')
                            yield Request(loupan_href, dont_filter=True, callback=self.parse_loupan)

    def parse_loupan(self,response):
        """
        解析每个城市所有楼盘
        :param response:
        :return:
        """
        global n
        print(response.status)
        if response.status == 200:
            html = etree.HTML(response.text)
            cons = html.xpath('//ul[@class="resblock-list-wrapper"]/li')
            loupan_url = response.url
            # 提取当前页
            obj = re.search(r'pg(\d+)/',loupan_url)
            if obj:
                n_num = obj.group(1)
                n_num = int(n_num) + 1
            else:
                n_num = 2
            # 提取最后一页
            n_page = html.xpath('//section[@class="se-part"][2]/div[@class="se-link-container"]/a[last()]')
            if n_page:
                last_page = (n_page[0].xpath('string(.)'))
            else:
                print('############')
                if n<1:
                    last_page = 1000000
                else:
                    last_page = None
                    n = 0
                n += 1
            print('last_page==',last_page,'andnum==',n_num)
            print('--------------------------------------------')
            if last_page and n_num <= int(last_page):
                for con in cons[:]:
                    item = urlItem()
                    id = con.xpath('./a/@href')[0]
                    title = con.xpath('./a/@title')
                    img = con.xpath('./a/img/@src')
                    item['id'] = id
                    item['title'] = title[0] if title is not None else ''
                    item['img_url'] = img[0] if img is not None else ''
                    yield item
                    print('---bk--this is base_url-----', loupan_url)
                    if 'pg' in loupan_url:
                        loupan_url = re.sub(r'pg(\d+)/', '', loupan_url)
                    detail = re.sub(r'/loupan/',id,loupan_url)
                    detail_href = detail + 'xiangqing/'
                    print(detail_href)
                    yield Request(detail_href, dont_filter=True, callback=self.parse_xianqing)
                if n_num == 2 and 'pg' not in loupan_url:
                    print('--------dengyu 2--------------')
                    if re.match(r'.*?loupan/',loupan_url):
                        n_href = loupan_url + 'pg2/'
                    else:
                        n_href = loupan_url + '/pg2/'
                else:
                    n_href = re.sub(r'pg(\d+)/', 'pg{n_num}/'.format(n_num=n_num), loupan_url)
                print(n_href, n_num, '----------this is next page!________')
                yield Request(n_href, dont_filter=True, callback=self.parse_loupan)
            else:
                print('end is  find')



    def parse_xianqing(self,response):
        """
        每个房详情页
        :param response:
        :return:
        """
        print(response.status,'------------parse_xiangqing---------------------------------')
        if response.status==200:
            html = etree.HTML(response.text)
            cons = html.xpath('//div[@class="big-left fl"]/h2')
            # print(cons)
            soup = BeautifulSoup(response.text,'lxml')
            base = response.url
            obj = re.search(r'.*?com(.*?)xiangqing/',base)
            if obj:
                href_id = obj.group(1)
                if soup:
                    title = soup.title.string
                else:
                    title = ''

                item = BeikeItem()
                item['id'] = href_id
                item['title'] = title
                # base_url = response.url
                print('title is ======',href_id)
                n = 1
                k = {1:'jb_info',2:'loupan_js',3:'loupan_guihua',4:'sm_zige',5:'peitao_info'}
                for con in cons[:]:
                    if n == 1:
                        dic = {}
                        lis = con.xpath('./following-sibling::ul[1]/li')
                        """
                     房屋基本信息   
                    """
                        h_type = lis[0].xpath('string(.)').strip().replace('\n','')
                        h_price = lis[1].xpath('string(.)').strip().replace('\n','')
                        h_teshe = lis[2].xpath('string(.)').strip().replace('\n','')
                        h_area = lis[3].xpath('string(.)').strip().replace('\n','')
                        loupan_doc = lis[4].xpath('string(.)').strip().replace('\n','')
                        soulou_doc = lis[5].xpath('string(.)').strip().replace('\n','')
                        kaifshang = lis[6].xpath('string(.)').strip().replace('\n','')
                        dic['h_type'] = h_type[0] if h_type is not None else ''
                        dic['h_price '] = h_price [0] if h_price  is not None else ''
                        dic['h_teshe'] = h_teshe[0] if h_teshe is not None else ''
                        dic['h_area'] = h_area[0] if h_area is not None else ''
                        dic['loupan_doc'] = loupan_doc[0] if loupan_doc is not None else ''
                        dic['soulou_doc'] = soulou_doc[0] if soulou_doc is not None else ''
                        dic['kaifshang'] = kaifshang[0] if kaifshang is not None else ''
                        item['jb_info'] = dic
                    else:
                        # print(cont ,'-------------------->this is cont')
                        cont = con.xpath('string(./following-sibling::ul[1])').strip().replace('\n','')
                        item[k[n]] = cont
                    n+=1
                print(item)
                yield item