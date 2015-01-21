# coding=utf-8
# Date=1/14/15
__author__ = 'MichaelZhao'

import MySQLdb
from MySQLdb.cursors import DictCursor


class DBEngine(object):
    __DBPool = None

    __DefaultDB = "mysql"
    __DefaultHost = "127.0.0.1"
    __DefaultUser = "root"
    __DefaultPasswd = "root"
    __DefaultPort = 3306
    __DefaultPoolOpen = True

    '''
    MinCached : 启动时开启的闲置连接数量(缺省值 0 以为着开始时不创建连接)
    MaxCached : 连接池中允许的闲置的最多连接数量(缺省值 0 代表不闲置连接池大小)
    MaxShared : 共享连接数允许的最大数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量,被请求为共享的连接将会被共享使用
    MaxConnections : 创建连接池的最大数量(缺省值 0 代表不限制)
    Blocking : 设置在连接池达到最大数量时的行为(缺省值 0 或 False 其他代表阻塞直到连接数减少,连接被分配)
    '''
    __MinCached = 20
    __MaxCached = 10
    __MaxShared = 20
    __MaxConnections = 50
    __Blocking = False

    '''
    DBEngine params
    @param db       数据库类型（mysql , oracle）
    @param host     数据库连接（default:127.0.0.1）
    @param port     数据库连接端口（default:3306）
    @param user     数据库用户
    @param passwd   数据库密码
    @param dateBase 数据库名称
    '''

    def __init__(self, **params):
        # 数据库链接设置
        self._db = DBEngine.__DefaultDB if params.get("db") is None else params["db"]
        self._host = DBEngine.__DefaultHost if params.get("host") is None else params["host"]
        self._port = DBEngine.__DefaultPort if params.get("port") is None else params["port"]
        self._user = DBEngine.__DefaultUser if params.get("user") is None else params["user"]
        self._passwd = DBEngine.__DefaultPasswd if params.get("passwd") is None else params["passwd"]

        if params.get("dateBase") is None:
            raise ValueError("Param dateBase can't be null when connect DB")
        self._dateBase = params["dateBase"]

        # 是否开启数据库连接池
        self._openPool = DBEngine.__DefaultPoolOpen if params.get("poolOpen") is None else params["poolOpen"]

        self._minCached = DBEngine.__MinCached if params.get("minCached") is None else params["minCached"]
        self._maxCached = DBEngine.__MaxCached if params.get("maxCached") is None else params["maxCached"]
        self._maxShared = DBEngine.__MaxShared if params.get("maxShared") is None else params["maxShared"]
        self._maxConnections = DBEngine.__MaxConnections if params.get("maxConnections") is None else params[
            "maxConnections"]
        self._blocking = DBEngine.__Blocking if params.get("blocking") is None else params["blocking"]

    '''
    数据库链接池设置
    '''

    def setPoolParams(self, params):
        self._minCached = DBEngine.__MinCached if params.get("minCached") is None else params["minCached"]
        self._maxCached = DBEngine.__MaxCached if params.get("maxCached") is None else params["maxCached"]
        self._maxShared = DBEngine.__MaxShared if params.get("maxShared") is None else params["maxShared"]
        self._maxConnections = DBEngine.__MaxConnections if params.get("maxConnections") is None else params[
            "maxConnections"]
        self._blocking = DBEngine.__Blocking if params.get("blocking") is None else params["blocking"]


    '''
    返回一个数据库的连接
    '''

    def connection(self):
        # dbUnit = None
        # if self._db == "mysql" :
        # import MySQLdb as dbUnit
        #
        # elif self._db == "oracle" :
        #     import Oracle as dbUnit

        # 是否使用连接池
        if self._openPool:
            return self.__get_connection(MySQLdb)
        else:
            if self._db == "mysql":
                return MySQLdb.connect(host=self._host, port=self._port, user=self._user, passwd=self._passwd,
                                       db=self._dateBase)

    '''
    从数据库连接池获取链接
    '''

    def __get_connection(self, dbUnit):
        if DBEngine.__DBPool is None:
            try:
                from DBUtils.PooledDB import PooledDB

                DBEngine.__DBPool = PooledDB(dbUnit, self._minCached, self._maxCached, self._maxShared,
                                             self._maxConnections,
                                             self._blocking, host=self._host, user=self._user, passwd=self._passwd,
                                             db=self._dateBase, charset="utf8")
            except Exception as e:
                raise Exception("Import DBUtils failed, error code:", e)

        return DBEngine.__DBPool.connection()

    '''
    数据库执行create操作
    '''

    def create(self, sql, params=(), connection=None, cursor=None, transactional=False):
        try:
            if connection is None:
                connection = self.connection()

            if cursor is None:
                cursor = connection.cursor(DictCursor)

            cursor.execute(sql, params)
            return cursor.lastrowid
        except Exception as e:
            raise Exception("Create sql deal failed, sql:%s, params:%s, Error code:%s" % (sql, params, e))
        finally:
            if not transactional:
                self.__db_close(cursor, connection)

    '''
    数据库执行批量操作
    '''

    def batchCreate(self, sql, params=(), connection=None, cursor=None, transactional=False):
        try:
            if connection is None:
                connection = self.connection()

            if cursor is None:
                cursor = connection.cursor(DictCursor)

            cursor.executemany(sql, params)
        except Exception as e:
            raise Exception("Batch create sql deal failed, sql:%s, params:%s, Error code:%s" % (sql, params, e))
        finally:
            if not transactional:
                self.__db_close(cursor, connection)

    '''
    数据更改操作
    '''

    def update(self, sql, params=(), connection=None, cursor=None, transactional=False):
        try:
            if connection is None:
                connection = self.connection()

            if cursor is None:
                cursor = connection.cursor(DictCursor)

            return cursor.execute(sql, params)
        except Exception as e:
            raise Exception("Update sql deal failed, sql:%s, params:%s, Error code:%s" % (sql, params, e))
        finally:
            if not transactional:
                self.__db_close(cursor, connection)

    '''
    数据库删除操作
    '''

    def delete(self, sql, params=(), connection=None, cursor=None, transactional=False):
        try:
            if connection is None:
                connection = self.connection()

            if cursor is None:
                cursor = connection.cursor(DictCursor)

            return cursor.execute(sql, params)
        except Exception as e:
            raise Exception("Delete sql deal failed, sql:%s, params:%s, Error code:%s" % (sql, params, e))
        finally:
            if not transactional:
                self.__db_close(cursor, connection)

    '''
    数据库查询操作
    '''

    def query(self, sql, params=(), connection=None, cursor=None, transactional=False):
        try:
            if connection is None:
                connection = self.connection()

            if cursor is None:
                cursor = connection.cursor(DictCursor)

            cursor.execute(sql, params)

            return cursor.fetchall()
        except Exception as e:
            raise Exception("Query sql deal failed, sql:%s, params:%s, Error code:%s" % (sql, params, e))
        finally:
            if not transactional:
                self.__db_close(cursor, connection)

    '''
    关闭sql的数据库连接
    '''

    def __db_close(self, cursor, connection):
        try:
            if cursor is not None:
                cursor.close()

            if connection is not None:
                connection.commit()
                connection.close()
        except Exception as e:
            raise Exception("Close DB resource failed, Error code", e)

    def __str__(self):
        return "----------------- DB Connection ------------------\n- DB: %s\n- Host: %s\n- User: %s\n- Passwd: %s\n- DateBase: %s\n- Port: %d\n" \
               "--------------------------------------------------" \
               % (self._db, self._host, self._user, self._passwd, self._dateBase, self._port)


'''
实现事务管理的db操作
'''


class TransactionManager(object):
    def __init__(self, **params):
        self.dbEngine = DBEngine(**params)
        self.connection = self.dbEngine.connection()
        self.cursor = self.connection.cursor(DictCursor)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
                self.cursor = None

            if self.connection is not None:
                self.connection.close()
                self.connection = None
        except Exception as e:
            raise Exception("Close DB resource failed, Error code", e)

    def query(self, sql, params=()):
        return self.dbEngine.query(sql, params, connection=self.connection, cursor=self.cursor, transactional=True)

    def create(self, sql, params=()):
        return self.dbEngine.create(sql, params, connection=self.connection, cursor=self.cursor, transactional=True)

    def update(self, sql, params=()):
        return self.dbEngine.update(sql, params, connection=self.connection, cursor=self.cursor, transactional=True)

    def delete(self, sql, params=()):
        return self.dbEngine.delete(sql, params, connection=self.connection, cursor=self.cursor, transactional=True)

    def batchCreate(self, sql, params=()):
        return self.dbEngine.batchCreate(sql, params, connection=self.connection, cursor=self.cursor,
                                         transactional=True)
