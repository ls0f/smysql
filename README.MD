## SMySQL

一个简单的MySQLdb orm封装，基本能覆盖常用的CURD操作。

### 安装

`pip install smysql`

### 使用

```
from smysql import DB, DBConfig

DBConfig.host = '127.0.0.1'
DBConfig.passwd = ''
DBConfig.user = 'root'
DBConfig.charset = 'utf8'

db = DB("test_db")
db.query('xxx')

```


### 测试


首先创建一个这样的表:

```
CREATE TABLE `user` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `version` int(11) DEFAULT '0',
  `name` varchar(20) DEFAULT NULL,
  `coin` int(11) DEFAULT '0',
  UNIQUE KEY `uid` (`uid`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
```

#### insert

创建小明的账户:

`uid = db.insert('user', obj_dict={"name": "小明", "coin": 0})`

假设小明的uid等于5

创建小红的账户:

`uid = db.insert('user', obj_dict={"name": "小红", "coin": 0})`

假设小明的uid等于6

#### update


将小明的金币改为100:

`db.update('user', query_dict={"uid": 5}, update_dict={'coin': 100})`

给小红加50个金币:

`db.update('user', query_dict={"uid": 6}, update_dict={'coin': DB.field("coin+50")})`

#### query

查询小明的金币:

`print db.query('user', query_dict={"uid": 5})[0]['coin']`

查询金币数量超过10个的用户的名字:

```
for item in db.query('user', query_dict={"coin__gt": 10}):  
    print item['name']
```

query 支持的比较符号有: 

* field__gt
* field__lt
* field__gte
* field__lte
* field__eq
* field__neq
* field__in
* field__like
* field__regexp


#### delete

删除小明的账户:

`db.delete("user", query_dict={"uid": 1})`

#### 事务

小明送小红10个金币:

```
db = DB("test_db", auto_trans=False)
db.update("user", query_dict={"uid": 5}, update_dict={"coin": DB.field("coin-10")})
db.update("user", query_dict={"uid": 6}, update_dict={"coin": DB.field("coin+10")})
db.end_trans()
```

如果小明要送小红100个金币呢？肯定要失败才行。

```
db = DB("test_db", auto_trans=False)
db.update("user", query_dict={"uid": 5, 'coin__gte': 100}, update_dict={"coin": DB.field("coin-100")}, sql_row_count=1)
db.update("user", query_dict={"uid": 6}, update_dict={"coin": DB.field("coin+100")},sql_row_count=1)
db.end_trans()
```

*sql\_row\_count* 表示必须要更新的记录条数，否则会抛出一个assert错误，然后回滚。


