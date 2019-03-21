import pymongo
import json, re
from functools import wraps
from time import sleep
from random import randint


def retry(*, times=3, max_wait=6,errors=(Exception,),handler=None):
	def decorate(func):

		@wraps(func)
		def wrapper(*args, **kwargs):
			for _ in range(times):
				try:
					return func(*args, **kwargs)
				except errors:
					sleep(randint(3,max_wait))
					if handler:
						handler(errors)

		return wrapper
	return decorate
# from mongo_help import insert_comp

client = pymongo.MongoClient('mongodb://47.106.211.81:27017')
db = client['CaiPiao']

def insert_comp(dic):
	db.com2.insert_one(dic)

def findone(num=None):
	return db.com2.find_one(num)
# def insert_comps(dic):
# 	db.com2.insert_many(dic, ordered=True)


# def find():
# 	return db.com1.find({'id':'1000'})



# def main():
# 	with open('./CP.json', encoding='utf-8') as f:
# 		s = f.read()
# 		kk = re.findall(r'{(.*?)}',s)
		# print(list(kk))
		# print(kk[1],kk[2])
		# for k in kk:
			# dic = {}
			# dic = (json.loads('{'+k+'}'))
			# insert_comp(dic)
	


# def test():
# 	for i in range(0,10):
# 		a = {"id":i}
# 		a = str(a)
# 		dic = (json.loads('{"w":'+str(i)+'}'))
# 		print(dic)

# if __name__ == '__main__':
	# test()
	# main()


