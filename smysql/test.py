from smysql import DB, DBConfig

DBConfig.host = '192.168.1.150'
DBConfig.passwd = ''
DBConfig.user = 'root'
DBConfig.charset = 'utf8'

db = DB("test_db")
db.query('user')