import os, sys
import getconfig
import GlobalData
import filePathAdj as fileabspath

class BaseObj(object):
    def __init__(self):
        self.__gObj = GlobalData.GlobalData()
        return

    def get_project_info_gobj(self):
        ipath = self.__gObj.get('ipath', None)
        opath = self.__gObj.get('opath', None)
        isdb = self.__gObj.get('isdb', None)
        isenc = self.__gObj.get('isenc', None)
        return ipath, opath, isdb, isenc
    
    def get_project_info_config(self):
        cfgObj = self.__gObj.get('configObj', None)
        if not cfgObj:
            cfgfile = self.__gObj.get('project_config', 'config.ini')
            cfgfname = fileabspath.filePathAdj().get_file_path(cfgfile)
            if os.path.isfile(cfgfname):
                cfgObj = getconfig.getconfig(cfgfname)
                self.__gObj.add('configObj', cfgObj)

        ipath = cfgObj.get_config('projectinfo', 'ipath')
        opath = cfgObj.get_config('projectinfo', 'opath')
        isdb = cfgObj.get_config('projectinfo', 'isdb')
        isenc = cfgObj.get_config('projectinfo', 'isenc')
        isdb = int(isdb)
        isenc = int(isenc)
        return ipath, opath, isdb, isenc

    def get_project_info(self):
        ipath, opath, isdb, isenc = self.get_project_info_gobj()
        if not opath:
            ipath, opath, isdb, isenc = self.get_project_info_config()
        return ipath, opath, isdb, isenc

    def debug(self):
        return

