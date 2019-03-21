from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree
import time,json
from JD_db_insert import *

chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 30)

def get_page(page):
	# browser.get('https://search.jd.com/Search?keyword=%E6%9C%BA%E5%99%A8%E4%BA%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=1&s=1&click=0')
	if page==1:
		url = 'https://www.jd.com'
		browser.get(url)
		input = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#key')))
		input.clear()
		input.send_keys('机器人')
		
		print('点击搜索按钮')
		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#search button.button')))
		submit.click()
		time.sleep(5)

	else:
		# 进入下一页
		input = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage .input-txt')))
		input.clear()
		input.send_keys(page)

		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage .btn.btn-default')))
		submit.click()

		time.sleep(2)

	 # 模拟操作滚动条
	for i in range(16):
		str_js = 'var step = document.body.scrollHeight / 16; window.scrollTo(0, step * %d)' % (i + 1)
		browser.execute_script(str_js)
		time.sleep(1)

	page_source = browser.page_source
	
	return page_source

def parse_page(page_source):

	"""获取商品信息"""

	html = etree.HTML(page_source)
	results = html.xpath('//li[@class="gl-item"]')
	list_data = []
	for result in results:
		dic = {}
		# print(result)
		img = result.xpath('.//div[@class="p-img"]/a/img/@src')
		price = result.xpath('.//div[@class="p-price"]//i/text()')
		shop_desc = result.xpath('.//div[@class="p-name p-name-type-2"]//em//text()')
		comment_num = result.xpath('.//div[@class="p-commit"]//a/text()')
		store = result.xpath('.//span[@class="J_im_icon"]/a/text()')
		store_link = result.xpath('.//span[@class="J_im_icon"]/a/@href')
		sku = result.xpath('./@data-sku')
		href = result.xpath('.//div[@class="p-img"]/a/@href')
		dic['sku'] = sku[0] if sku else ''
		dic['img'] = img[0] if img else ''
		dic['price'] = price[0] if price else ''
		dic['shop_desc'] = ''.join(shop_desc) if shop_desc else ''
		dic['comment_num'] = comment_num[0] if comment_num else ''
		dic['store'] = store[0] if store else ''
		dic['href'] = href[0] if href else ''
		dic['store_link'] = store_link[0] if store_link else ''
		# dic['page'] = str(page)
		list_data.append(dic)

	print('准备插入数据')
	insert(db,cursor,list_data)



def main():
	# 爬取100页商品
	for i in range(1,101):
		pages = get_page(i)
		# print(page_num)
		parse_page(pages)



if __name__ == '__main__':
	db = get_con()
	cursor = get_cursor(db)
	main()
	close(db)

