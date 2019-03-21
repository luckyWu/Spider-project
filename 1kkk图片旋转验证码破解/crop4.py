from PIL import Image
from io import BytesIO
import os

def crop4():
	"""获取每一个头像"""
	lists = os.listdir('./kkk_images') # 获取目录下所有文件
	m = 0
	for li in lists:
		screenshot = Image.open('%s/%s' % ('./kkk_images', li))
		crop_image = screenshot.crop((0, 0, 304, 76))
		for i in range(0,4):
			# 每个小图头像宽高都是76个像素
			crop_image = screenshot.crop((i*76, 0, (i+1)*76, 76))
			file_name = './small_pic1/'+'m'+str(m)+'.png'
			crop_image.save(file_name)
			m = m +1

if __name__ == "__main__":
	crop4()