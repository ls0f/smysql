#coding:utf-8

from simple_mysql import DB, DBConfig

DBConfig.host = '192.168.1.150'

db = DB("test_db")

# xiaoming = db.insert('user', obj_dict={"name": "小明", "coin": 0})
# xiaohong = db.insert('user', obj_dict={"name": "小红", "coin": 0})


# db.update('user', query_dict={"uid": 6}, update_dict={'coin': DB.field("coin+50")})

# print db.query('user', query_dict={"uid": 5})[0]['coin']


# for item in db.query('user', query_dict={"coin__gt": 10}):
    # print item['name']

# db.delete("user", query_dict={"uid": 1})

db = DB("test_db", auto_trans=False)
db.update("user", query_dict={"uid": 6}, update_dict={"coin": DB.field("coin+100")},sql_row_count=1)
db.update("user", query_dict={"uid": 5, 'coin__gte': 100}, update_dict={"coin": DB.field("coin-100")}, sql_row_count=1)
db.end_trans()

