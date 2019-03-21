import pymongo

client = pymongo.MongoClient('10.7.153.121',27017)
db = client.qichamao

def insert_comp(dic):
	db.comy.insert_one(dic)