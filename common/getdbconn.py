import os, sys
import common.GlobalData as GlobalData
import common.getconn as getconn

class getdbconn(object):
    def __init__(self, dbconnstr=None):
        self.__cfgObj = {}
        self.__dbconnObj = self.__get_db(dbconnstr)
        return

    def __get_db(self, dbconnstr):
        gObj = GlobalData.GlobalData()
        kdbconnstr = dbconnstr if dbconnstr else gObj.get('dbconn', None)
        if not kdbconnstr:
            raise ValueError, 'dbconnstr not defined...'
        conntype, dbhost, dbport, dbuser, dbpasswd, dbname = kdbconnstr.strip('#').split("#")
        dbconnObj = getconn.getconn(conntype, dbhost, dbport, dbuser, dbpasswd, dbname)
        return dbconnObj

    def getconn(self):
        return self.__dbconnObj.getconn()

    def close(self):
        return self.__dbconnObj.close()

    def debug(self):
        return

if __name__=='__main__':
    obj = getdbconn()
    print obj.getconn()

