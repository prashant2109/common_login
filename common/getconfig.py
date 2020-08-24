import os, sys
import ConfigParser
import GlobalData
import cStringIO

class getconfig(object):
    def __init__(self, cfgfile):
        self.__cfgObj = self.__load_config(cfgfile)
        return

    def __read_idata(self, fname):
        fbuf = ''
        if os.path.isfile(fname): 
            fd = open(fname, 'r')
            fbuf = fd.read()
            fd.close()
        return fbuf

    def __load_config(self, cfg_file):
        gObj = GlobalData.GlobalData()
        head, fname = os.path.split(cfg_file)
        cfgObj = gObj.get(fname, None)
        if cfgObj: return cfgObj

        buf = self.__read_idata(cfg_file)
        if buf:
            #if not os.path.isfile(cfg_file):
            #    raise ValueError, '%s, config file not found...' %(cfg_file)
            cfgObj = ConfigParser.SafeConfigParser()
            #cfgObj.read(cfg_file)
            cfgObj.readfp(cStringIO.StringIO(buf))
            gObj.add(fname, cfgObj)
            return cfgObj
        return {}

    def get_config(self, section, name):
        if self.__cfgObj:
            val = self.__cfgObj.get(section, name)
            if val:
                return val.strip()
        return None

    def get(self, section, name):
        return self.get_config(section, name)

    def get_project_info(self):
        ipath = self.get_config('projectinfo', 'ipath')
        opath = self.get_config('projectinfo', 'opath')
        isdb = self.get_config('projectinfo', 'isdb')
        isenc = self.get_config('projectinfo', 'isenc')
        isdb = int(isdb)
        isenc = int(isenc)
        return ipath, opath, isdb, isenc

    def debug(self):
        return

if __name__=='__main__':
    cfgfile = 'config.ini'
    obj = getconfig(cfgfile)
    print obj.get_config('project_input', 'ipath')

