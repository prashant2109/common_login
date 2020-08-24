import os, sys
import decimal
import uuid
#import _mssql

class getconn(object):
    def __init__(self, conntype, dbhost, dbport, dbuser, dbpasswd, dbname):
        self.__conntype = conntype[:]
        self.__dbhost = dbhost[:]
        self.__dbport = dbport[:]
        self.__dbuser = dbuser[:]
        self.__dbpasswd = dbpasswd[:]
        self.__dbname = dbname[:]
        self.__conn, self.__cur = self.__get_conn()
        return

    def __get_mysql_conn(self):
        import MySQLdb
        MySQLdb.fetchReturnsList = 1
        MySQLdb.noPostgresCursor = 1
        conn = MySQLdb.connect(self.__dbhost, self.__dbuser, self.__dbpasswd, self.__dbname)
        cur = conn.cursor()
        return conn, cur

    def __get_mssql_conn(self):
        import pymssql
        conn = pymssql.connect(host=self.__dbhost, user=self.__dbuser, password=self.__dbpasswd, database=self.__dbname)
        cur = conn.cursor()
        return conn, cur

    def __get_conn(self):
        if self.__conntype == 'mysql':
            return self.__get_mysql_conn()
        elif self.__conntype == 'mssql':
            return self.__get_mssql_conn()
        else:
            raise ValueError, 'invalid conn type...'
        return None, None

    def getconn(self):
        return self.__conn, self.__cur

    def close(self):
        if self.__conntype == 'mysql' and self.__conn:
            self.__cur.close()
            self.__conn.close()
        elif self.__conntype == 'mssql' and self.__conn:
            self.__cur.close()
            self.__conn.close()
        self.__cur = None
        self.__conn = None
        return

    def debug(self):
        return

