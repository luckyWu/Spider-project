import pymysql

def get_con():
	host = '127.0.0.1'
	port = 3306
	user = 'root'
	password = '123456'
	database = 'JD'
	db = pymysql.connect(host=host,user=user,password=password,database=database,charset='utf8',port=port)
	return db

# 获取游标
def get_cursor(db):
	cursor = db.cursor()
	return cursor

# 插入数据
def insert(db,cursor,lists):
	for item in lists:
		print('进入sql语句')
		cursor.execute( query='insert into jd_data(img,price,shop_desc,commentNum,store,sku,href,store_link)values(%s,%s,%s,%s,%s,%s,%s,%s)',
                args=(item['img'],item['price'],item['shop_desc'],
				item['comment_num'],item['store'],item['sku'],item['href'],item['store_link']))
		db.commit()


def close(db):
	# 关闭连接
	db.close()


if __name__ == '__main__':
	db = get_con()
	cursor = get_cursor(db)
	result = cursor.execute(query='select * from mogu')
	# cursor.execute(query='alter table mogu add column free varchar(50)')
	datas = cursor.fetchall() # yuanzu
	new_id = 0
	for data in datas:
		new_id +=1
		print(data[0])
		cursor.execute(query='update mogu set free=%s where id=%s',args=(new_id,data[0]))
		db.commit()
		print(new_id)
