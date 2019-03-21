from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree
from PIL import Image
from io import BytesIO
from chaojiying import main1
import time


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless') 无头浏览器
browser = webdriver.Chrome(chrome_options=chrome_options)
# browser = webdriver.PhantomJS()
# browser = webdriver.Chrome()
browser.set_window_size(1400, 700)
# 显式等待 针对某个节点的等待
wait = WebDriverWait(browser, 10)

def get_page():
    url = 'https://login.10086.cn/html/register/register.html'
    browser.get(url)
    html = browser.page_source
    return html


def get_big_image():
    """取浏览器窗口内全图"""

    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot


def get_position():
	"""取验证码坐标位置（左上角和右下角）"""
	img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#captchaImg')))
	loc = img.location
	size = img.size
	print(loc)
	print(size)
	x1 = loc['x']
	y1 = loc['y']
	x2 = loc['x'] + size['width']
	y2 = y1 + size['height']
	print(x1,y1,x2,y2)
	return (x1, y1, x2, y2)

def parse_html(html):
    # etree_html = etree.HTML(html)
    screenshot = get_big_image()
    screenshot.save('full_screen.png')
    x1, y1, x2, y2 = get_position()
    crop_image = screenshot.crop((x1, y1, x2, y2)) #获取验证码图片
    file_name = 'crop.png'
    crop_image.save(file_name)
    captha_str = main1(file_name) # 获取验证码
    
    # 用户名和密码
    username = '2418717998@qq.com'
    password = '12345678a'

    print(captha_str)
    # 选择节点
    input_emailname = wait.until(EC.presence_of_element_located
                       ((By.CSS_SELECTOR, 'input#loginName')))
    input_password1 = wait.until(EC.presence_of_element_located
                       ((By.CSS_SELECTOR, 'input#newPassword')))
    input_password2 = wait.until(EC.presence_of_element_located
                                 ((By.CSS_SELECTOR, 'input#newPasswordRepeat')))
    input_check = wait.until(EC.presence_of_element_located
                             ((By.CSS_SELECTOR, 'input#inputCode')))
    print('s1')
    sublime1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#regText_bg_new')))
    print('s2')
    sublime2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#regText_bg_person')))
    print('s3')
    sublime = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.reg_btn.clearfix')))

    # 模拟登陆
    input_emailname.send_keys(username)
    input_password1.send_keys(password)
    input_password2.send_keys(password)
    input_check.send_keys(captha_str)

    time.sleep(2)
    sublime1.click()
    time.sleep(2)
    sublime2.click()
    time.sleep(2)
    sublime.click()
    time.sleep(2)
    html = browser.page_source

def main():
	html = get_page()
	parse_html(html)

if __name__ == '__main__':
	main()