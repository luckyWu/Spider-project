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
	for i in range(200):
		time = 1543563120000+i
		url = 'http://www.1kkk.com/image3.ashx?t='+str(time)+'&quot'
		res = requests.get(url,headers=headers)
		print(res.status_code)
		content = res.content
		name = 'm'+str(i)
		with open('./kkk_images/%s.png' % name,'wb') as f:
			f.write(content)
			print(i)
get_pic()

def del_repeat():
    """将small_pic复制内容至small_pic_result，分别执行遍历和删除操作"""
    print('开始去重')
    n = 0
    del_count = 0
    list_image_name = os.listdir('./small_pic')
    for index in range(len(list_image_name)):
        try:
            # 原图比较
            for index_temp in range(index+1,len(list_image_name)):
                score = get_compare('./small_pic/%s'%list_image_name[index], './small_pic/%s'%list_image_name[index_temp])
                print(n)
                n +=1
                if int(score) >= 85:
                    os.remove('./small_pic_result/%s'%list_image_name[index_temp])
                    del_count += 1
                    print('删除%d张图片'%del_count)

            # 旋转三次，继续去重
            for _ in range(3):
                img = Image.open('./small_pic/%s'%list_image_name[index])
                img_new = img.rotate(90)
                img_new.save('./small_pic/%s'%list_image_name[index])
                for index_temp in range(index+1,len(list_image_name)):
                    score = get_compare('./small_pic/%s'%list_image_name[index], './small_pic/%s'%list_image_name[index_temp])
                    print(n)
                    n += 1
                    if int(score) >= 85:
                        os.remove('./small_pic_result/%s'%list_image_name[index_temp])
                        del_count += 1
                        print('删除%d张图片'%del_count)
        except Exception:
            continue
    print('本次去重%d张图片.'%del_count)

def mutis_repeat(rotate,num):

	rotate = 90
	list_remove = set()
	list1_remove = set()
	list2_remove = set()
	lists = os.listdir('./small_pic1')
	print(lists)
	lenth = len(lists)-1
	count = 0
	for i in range(lenth):
		img_url = '%s/%s' % ('./small_pic%s/'%num, lists[i])
		img1 = Image.open(img_url)
		out = img1.rotate(rotate)
		# out.save(img_url)
		k = i+1
		for j in range(k,lenth+1):
			src1 = './small_pic%s/'%num+lists[i]
			src2 = './small_pic%s/'%num+lists[j]
			if src1 in list_remove:
				continue
		
			score = get_compare2(out,src2)
			count += 1
			print('i=%s , j=%s , score=%s' %(lists[i],lists[j],score))
			if score>90:
				list_remove.add(src2)
				# list1_remove.add(src1)
				list2_remove.add((src1,src2))


	con = list(list_remove)
	cont = json.dumps(con)
	with open('./samenan%s.json'%num,'w',encoding='utf-8') as f:
		json.dump(cont,f)

	# con1 = list(list1_remove)
	# cont1 = json.dumps(con1)
	# with open('./same1m.json','w',encoding='utf-8') as f:
	# 	json.dump(cont1,f)

	con3 = list(list2_remove)
	cont3 = json.dumps(con3)
	with open('./samemam%s.json'%num,'w',encoding='utf-8') as f:
		json.dump(cont3,f)
	# print(con,con1)

def crop4():
	lists = os.listdir('./kkk_images')
	m = 0
	for li in lists:
		screenshot = Image.open('%s/%s' % ('./kkk_images', li))
		crop_image = screenshot.crop((0, 0, 304, 76))
		for i in range(0,4):
			crop_image = screenshot.crop((i*76, 0, (i+1)*76, 76))
			file_name = './small_pic1/'+'m'+str(m)+'.png'
			crop_image.save(file_name)
			m = m +1
		# file_name = './small_pic/'+li
		# crop_image.save(file_name)


def crop1():
	lists = os.listdir('./vip_big')
	k = 1
	for li in lists:
		screenshot = Image.open('%s/%s' % ('./vip_big', li))
		for i in range(0,4):
			crop_image = screenshot.crop((i*76, 0, (i+1)*76, 76))
			file_name = './small_pic/'+str(k)+'.png'
			crop_image.save(file_name)
			k += 1

def xuan(num,rotate):
	src = './small_pic1/'+str(num)+'.png'
	screenshot = Image.open(src)
	out=screenshot.rotate(rotate)
	file_name = './small_pic1/'+str(num)+'.png'
	#out.show()
	out.save(file_name)

def main():

	rotate = 90
	list_remove = set()
	list1_remove = set()
	list2_remove = set()
	lists = os.listdir('./small_pic1')
	print(lists)
	lenth = len(lists)-1
	count = 0
	for i in range(lenth):
		for n in range(4):
			img_url = '%s/%s' % ('./small_pic1/', lists[i])
			img1 = Image.open(img_url)
			out = img1.rotate(rotate)
			out.save(img_url)
			k = i+1
			for j in range(k,lenth+1):
				src1 = './small_pic1/'+lists[i]
				src2 = './small_pic1/'+lists[j]
				if src1 in list_remove:
					continue
			
				score = get_compare(src1,src2)
				count += 1
				print('i=%s , j=%s , score=%s' %(lists[i],lists[j],score))
				if score>90:
					list_remove.add(src2)
					list1_remove.add(src1)
					list2_remove.add((src1,src2))
	con = list(list_remove)
	cont = json.dumps(con)
	with open('./samen.json','w',encoding='utf-8') as f:
		json.dump(cont,f)

	con1 = list(list1_remove)
	cont1 = json.dumps(con1)
	with open('./same1m.json','w',encoding='utf-8') as f:
		json.dump(cont1,f)

	con3 = list(list2_remove)
	cont3 = json.dumps(con3)
	with open('./same2n.json','w',encoding='utf-8') as f:
		json.dump(cont3,f)
	# print(con,con1)
# def search(rotate,lenth,file_num):
# 	global list_remove
# 	for i in range(lenth-1):
# 		img_url ='./small_pic'+str(file_num)+'/'+lists[i]
# 		img1 = Image.open(img_url)
# 		out = img1.rotate(rotate)
# 		out.save(img_url)
# 		k = i+1
# 		for j in range(k,lenth):
# 			src1 = './small_pic'+str(file_num)+'/'+lists[i]
# 			src2 = './small_pic'+str(file_num)+'/'+lists[j]
# 			score = get_compare(src1,src2)
# 			print('i=%s , j=%s , score=%s' %(lists[i],lists[j],score))
# 			if score>90:
# 				list_remove.add(src2)



# 	print(list_remove)
if __name__ == '__main__':
	start = time.time()
	# crop1()
	# #main()

	# p1 = Process(target=mutis_repeat, args=(90,1))
	# p2 = Process(target=mutis_repeat, args=(270,2))
	# p3 = Process(target=mutis_repeat, args=(180,3))
	# p4 = Process(target=mutis_repeat, args=(0,4))
	
	# p1.start()
	# p2.start()
	# p3.start()
	# p4.start()

	# p1.join()
	# p2.join()
	# p3.join()
	# p4.join()
	# del_repeat()
	end = time.time()

	
	print(end-start)
	# with open('./same.json','r',encoding='utf-8') as f:
	# 	content = json.load(f)
	# 	content = json.loads(content)
	# 	print(len(content),type(content))
	# 	for remove_pic in content:
	# 		os.remove(remove_pic)

	# 	print('shanchu chenggong!!!!!!!!!!!!!')



	# print(lists)
	# for li in lists:
	# 	for i in range(0,4):
		

		
# num1 = 1026
# 	num2 = 1010
# 	src1 = './small_pic1/'+str(num1)+'.png'
# 	src2 = './small_pic1/'+str(num2)+'.png'

# 	score = get_compare(src1,src2)
# 	print(score)