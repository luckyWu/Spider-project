from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree
from PIL import Image
from io import BytesIO
import requests
import os
import time,threading
from compare_helper import get_compare
import json


chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 5)

def get_big_image():
    # browser.execute_script('window.scrollTo(0, 300)')
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot

# 取验证码坐标位置（左上角和右下角）
def get_position():
	imgs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="form-wrap"]//div[@class="rotate-background"]')))
	print(imgs)
	lists = []
    # 第一张图片验证码的坐标
	for img in imgs:

		x1 = img.location['x']
		y1 = img.location['y']
		x2 = img.size['width']
		y2 = img.size['height']	
		lists.append((x1,y1,x1+x2,y1+y2))
		print(x1,y1,x1+x2,y1+y2)	
	return lists

def get_page():
	#点击弹出登陆框
	submit = wait.until(
	EC.element_to_be_clickable((By.CSS_SELECTOR, '.header-avatar'))
	)

	submit.click()
	i = 1
	time.sleep(2) #等待登录框出现
	screenshot = get_big_image()
	screenshot.save('full_screen.png')
	list_all = get_position()
	img_obj = []
	for li in list_all:
		crop_image = screenshot.crop(li)
		img_url = './'+'m'+str(i)+'.png'
		crop_image.save(img_url)
		i += 1
		img_obj.append(img_url)
		# img_obj.append(crop_image)

	#准备进入输入操作

	input = wait.until(
		EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="txt_name"]')))
	input.clear()
	input.send_keys(user)

	input = wait.until(
	EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="txt_password"]')))
	input.clear()
	input.send_keys(pw)
	
	#确定点击事件
	submit = wait.until(
	EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="btnLogin"]')))

	# 换一组图片
	reset = wait.until(
	EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="rotate-refresh"')))

	
	lists = os.listdir('./small_pic1')
	lenth = len(lists)
	sucess = 0
	k=0
	rotate_backgrounds = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="form-wrap"]/div/div[@class="rotate-background"]')))
	# 旋转对比
	for img in rotate_backgrounds:
		print('into---------')
		for n in range(4):
			flag = False
			for li in lists:
				img_url = '%s/%s' % ('./small_pic1/', li)
				# 
				s = get_compare(img_obj[k], img_url)
				print(k, img_obj[k],img_url,s)
				if s>90:
					print(s)
					flag = True
					sucess += 1
					break
			if flag==True:
				break
			img.click()
			# 旋转后再在图片库中比较
			img1 = Image.open(img_obj[k])
			out = img1.rotate(-90)
			out.save(img_obj[k])
		k+=1

	if sucess==4:
		print('成功！')
		submit.click()
	else:
		print('失败')
		# reset.click()
		# get_page()

if __name__ == "__main__":

	url = 'http://www.1kkk.com'
	browser.get(url)
	print('网址获取成功！！！！！！！！！！！！！！')
	user = '2222@qq.com'
	pw = '123456'
	get_page()
