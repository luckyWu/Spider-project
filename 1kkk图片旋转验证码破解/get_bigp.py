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
from compare_helper import get_compare2
import json
from multiprocessing import Process
import os
headers = {
		
"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/52.0.2743.116 Safari/537.36",

		}

def get_pic():
	for i in range(300):
		time = 1553563120000+i
		url = 'http://www.1kkk.com/image3.ashx?t='+str(time)+'&quot'
		res = requests.get(url,headers=headers)
		print(res.status_code)
		content = res.content
		name = 'm'+str(i)
		with open('./kkk_images/%s.png' % name,'wb') as f:
			f.write(content)
			print(i)

get_pic()