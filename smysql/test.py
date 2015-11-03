from smysql import DB, DBConfig

DBConfig.host = '192.168.1.150'
DBConfig.passwd = ''
DBConfig.user = 'root'
DBConfig.charset = 'utf8'

db = DB("test_db")
print db.query('user', print_sql=True, page=0)

db.update("user",query_dict={'uid': 2}, update_dict={"name": "xxx"}, sql_row_count=2)