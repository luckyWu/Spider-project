import requests
import json, re
import time
import datetime
from lxml import etree
from mongo_help import insert_comp,retry
from random import randint
from agent_helper import get_random_agent
k = 1
headers = {'User-Agent':get_random_agent()
}
# f = open('CP.csv','a')
# f_csv = csv.writer(f)
	
@retry()
def get(date):
	global k
	url = 'http://caipiao.163.com/award/cqssc/'+date+'.html'
	res = requests.get(url, headers=headers, timeout=8)
	print('------------------------------------')
	if res.status_code==200:	
		lists =[]
		html = res.content.decode('utf-8')
		con = etree.HTML(html)
		tr = con.xpath('//div[@class="lottery-results"]')[0]
		num = tr.xpath('.//td[@class="award-winNum"]/text()') #开奖号码
		td1 = tr.xpath('.//td[@class="award-winNum"]//following-sibling::td[1]/text()') # 十位
		td2 = tr.xpath('.//td[@class="award-winNum"]//following-sibling::td[2]/text()') # 个位
		td3 = tr.xpath('.//td[@class="award-winNum"]//following-sibling::td[3]/text()') # 后三形态
		length = len(num)
		for n in range(0,length):
			dic = {}
			dic['id'] = k 
			dic['issue'] = n+1 # 期号
			dic['num'] = num[n]
			dic['tenth'] = td1[n]
			dic['bit'] = td2[n]
			dic['last3'] = td3[n]
			# f_csv.writerow([k,n+1,num[n],td1[n],td2[n],td3[n]])
			lists.append(dic)
			k += 1
		return lists

import datetime

def main():
	tstart_str = '2015-03-01 00:00:00'
	tend_str = '2015-03-02 00:00:00' 
	# 日期格式转化为字符串格式 
	dstart = datetime.datetime.strptime(tstart_str, '%Y-%m-%d %H:%M:%S') 
	dend = datetime.datetime.strptime(tend_str, '%Y-%m-%d %H:%M:%S') 
	# print(dend,type(dend))
	# now = datetime.datetime.now()

	while dstart < dend: 
	    a = dstart.strftime('%Y-%m-%d')
	    print(a)
	    date = a.replace('-','')
	    res = get(date)
	    dics = {}
	    dics['_id'] = date
	    dics[date] = res
	    insert_comp(dics)
	    delta = datetime.timedelta(days=1) 
	    dstart = dstart + delta # 返回的是datetime型


if __name__ == "__main__":
	s = time.time()
	main()
	e = time.time()
	print(f'{e-s}秒')