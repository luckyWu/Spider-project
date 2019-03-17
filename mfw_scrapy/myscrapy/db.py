import pymysql

def get_con():
    """连接数据库"""
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = '123456'
    database = 'mfw_trip1'
    db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8mb4', port=port)
    return db

def get_cursor(db):
    """获取游标对象"""
    cursor = db.cursor()
    return cursor

def insert(db, cursor, item):
    """插入数据"""
    cursor.execute(
        query='insert into commits(title, content, zan, user_name) values (%s,%s,%s,%s)',
        args=( item['title'], item['content'], item['zan'], item['user_name']))
    db.commit()

if __name__ == '__main__':
    db = get_con()
    cursor = get_cursor(db)
    item = {}
    item['title'] = 1
    item['content'] = 1
    item['zan'] = 1
    item['user_name'] = 1
    insert(db,cursor,item )