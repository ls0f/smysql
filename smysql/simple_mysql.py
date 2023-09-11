#coding:utf-8

import logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("smysql")
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
except ImportError:
    import MySQLdb



class DBConfig(object):

    # mysql 配置
    host = "127.0.0.1"
    port = 3306
    passwd = ""
    charset = "utf8"
    user = "root"


class Field(object):

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string


class DB(object):

    def __init__(self, db_name, conn=None, auto_trans=True, *args, **kwargs):
        super(DB, self).__init__()
        self.db_name = db_name
        self.conn = conn
        if auto_trans is True:
            self._trans_end = True
        else:
            self._trans_end = False

        if conn is None:
            self.auto_close_conn = True
        else:
            self.auto_close_conn = False

    @staticmethod
    def field(f):
        return Field(f)

    def end_trans(self):

        self._trans_end = True
        with self:
            pass

    def call_after_commit(self):
        pass

    def __enter__(self):

        if self.conn is None:
            self.conn = DB.get_conn(self.db_name)

        self.cur = self.conn.cursor()

    def __exit__(self, exc, value, tb):

        self.cur.close()
        if exc:
            self.conn.rollback()
            self.call_after_commit()
        else:
            if self._trans_end is True:
                self.conn.commit()
                self.call_after_commit()

        if self.auto_close_conn and self._trans_end is True:
            self.close_conn()

    def close_conn(self):

        # 关闭连接
        self.conn.close()
        self.conn = None

    def test_with_ok(self):

        with self:
            print('i am ok ')

    def test_with_error(self):
        with self:
            print('i am wrong')
            assert 1==2

    @staticmethod
    def get_conn(db_name):

        conn = MySQLdb.connect(db=db_name,
                               host=DBConfig.host,
                               passwd=DBConfig.passwd,
                               charset=DBConfig.charset,
                               port=DBConfig.port,
                               user=DBConfig.user)
        return conn

    def insert(self, table_name, obj_dict, mode='insert', print_sql=False):
        try:
            assert mode in ("insert", 'replace', 'insert_or_update')
        except AssertionError:
            LOGGER.error("mode must be in `insert`、`replace`、`insert_or_update`")
            raise
        placeholders = ', '.join(['%s'] * len(obj_dict))
        columns = ', '.join(obj_dict.keys())
        args = tuple(obj_dict.values())
        start = ''
        if mode == 'insert' or mode == 'insert_or_update':
            start = "INSERT INTO "
        elif mode == 'ignore':
            start = 'INSERT IGNORE INTO '
        elif mode == 'replace':
            start = "REPLACE INTO "
        else:
            raise
        sql = "%s %s ( %s ) VALUES ( %s )" % (start, table_name, columns, placeholders)

        if mode == "insert_or_update":
            update = ['%s=%s' % (key, '%s') for key in obj_dict.keys()]
            sql += " ON DUPLICATE KEY UPDATE %s" % (','.join(update),)
            args = args*2

        if print_sql:
            LOGGER.debug("sql:{}".format(sql))
            LOGGER.debug("args:{}".format(args))

        with self:
            self.cur.execute(sql, args=args)
            last_id = self.conn.insert_id()
            return last_id

    def update(self, table_name, query_dict, update_dict, print_sql=False, sql_row_count=0):
        # 添加a=a+1和a=a-1的支持
        query, args = DB.gen_sql_query(query_dict)
        update = ', '.join(['%s=%s' % (key, str(value) if isinstance(value, Field) else '%s')
                            for key, value in update_dict.items()])
        args = [item for item in update_dict.values() if isinstance(item, Field) is False] + args
        sql = "update %s set %s %s " %(table_name, update, query)
        if print_sql:
            LOGGER.debug("sql:{}".format(sql))
            LOGGER.debug("args:{}".format(args))

        with self:
            row_count = self.cur.execute(sql, args=args)
            try:
                assert sql_row_count == 0 or row_count == sql_row_count
            except AssertionError:
                LOGGER.error("{} don't effect {} rows".format(sql, sql_row_count))
                raise
        return row_count

    def delete(self, table_name, query_dict, print_sql=False, sql_row_count=0):

        query, args = DB.gen_sql_query(query_dict)
        sql = "delete from %s %s" % (table_name, query)

        if print_sql:
            LOGGER.debug("sql:{}".format(sql))
            LOGGER.debug("args:{}".format(args))

        with self:
            row_count = self.cur.execute(sql, args=args)
            try:
                assert sql_row_count == 0 or row_count == sql_row_count
            except AssertionError:
                LOGGER.error("{} don't effect {} rows".format(sql, sql_row_count))
                raise

        return row_count

    def query(self, table_name,query_dict={},fields=['*'],page=0,page_num=50,
                       group_by='',order_by='',print_sql=False, slave=False):

        if page == 0:
            page_p = " "
        else:
            start = page*page_num-page_num
            page_p = " limit %s,%s" % (start, page_num)

        query, args = DB.gen_sql_query(query_dict)
        sql = "select %s from %s %s %s %s %s" % (','.join(fields), table_name, query, group_by, order_by, page_p)
        if print_sql:
            LOGGER.debug("sql:{}".format(sql))
            LOGGER.debug("args:{}".format(args))

        with self:
            self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cur.execute(sql, args=args)
            result = self.cur.fetchall()
            return result

    def exec_sql(self, sql, args=None):

        with self:
            self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cur.execute(sql, args=args)
            result = self.cur.fetchall()
            return result

    @staticmethod
    def gen_sql_query(query_dict):

        query = ""
        if not query_dict:
            return query,None

        args = []
        for key, value in query_dict.items():
            key = key.split("__")
            op = key[1] if len(key) == 2 else 'eq'
            sql_operator = DB.get_sql_operator(op)

            if not query:
                place = "where"
            else:
                place = "and"

            if sql_operator == 'in':
                query += " %s %s in (%s)" % (place, key[0], ','.join(['%s']*len(value)),)
                args.extend(list(value))
            elif sql_operator == 'nin':
                query += " %s %s not in (%s)" % (place, key[0], ','.join(['%s']*len(value)),)
                args.extend(list(value))
            elif sql_operator == 'sql':
                query += " %s %s" % (place, value)
            elif isinstance(value, Field):
                query += " %s %s %s %s" % (place, key[0], sql_operator, value)
            else:
                query += " %s %s %s %s" % (place, key[0], sql_operator, '%s')
                args.append(value)

        return query,args

    @staticmethod
    def get_sql_operator(op):

        operator_dict = {
            'gt': '>',
            'gte': '>=',
            'eq': '=',
            'neq': '!=',
            'lt': '<',
            'lte': '<=',
            'in': 'in',
            'nin': 'nin',
            'like': 'like',
            'regexp': 'regexp',
            'sql': 'sql',
        }

        try:
            assert op in operator_dict
        except AssertionError:
            LOGGER.error("not supported operator")
            raise

        return operator_dict[op]


