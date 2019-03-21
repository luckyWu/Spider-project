
from PIL import Image
from io import BytesIO
import os
from compare_helper import get_compare
list_remove = set() #添加相似的图片地址
def Dupli():
	"""去重"""

	rotate = 90 #每次旋转90度
	lists = os.listdir('./small_pic1')
	# print(lists)
	lenth = len(lists)-1
	for i in range(lenth-1):
		for n in range(4):
			# 每旋转1次与后面的对比
			img_url ='./small_pic1' + '/'+lists[i]
			img1 = Image.open(img_url)
			out = img1.rotate(rotate)
			out.save(img_url)
			k = i+1
			for j in range(k,lenth):
				src1 = './small_pic1' + '/' + lists[i]
				src2 = './small_pic1' + '/' + lists[j]
				if src2 in list_remove:
					continue
				score = get_compare(src1,src2)
				print('i=%s , j=%s , score=%s' %(lists[i],lists[j],score))

				# 相似度90以上删除
				if score>90:
					list_remove.add(src2)

def rem():
	for remove_pic in list_remove:
		os.remove(remove_pic) #删除文件
	print('shanchu chenggong!!!!!!!!!!!!!')

if __name__ == "__main__":
	Dupli()
	rem()