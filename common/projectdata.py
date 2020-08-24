import os, sys

def get_render_url_path(urlid, cfgObj, urlflag=None):
        renderurlbasepath = cfgObj.get_config('renderinfo', 'renderurlbasepath')
        renderbasepath = cfgObj.get_config('renderinfo', 'renderbasepath')
        renderprefix = cfgObj.get_config('renderinfo', 'renderurlprefix')
        render_outdir = cfgObj.get_config('renderinfo', 'renderoutputdir').lstrip('/')
        render_imgdir = cfgObj.get_config('renderinfo', 'renderimagedir').lstrip('/')
        rbasepath = renderurlbasepath if urlflag else renderbasepath
        urldir = '%s%s'%(str(renderprefix), str(urlid))
        render_url_path = os.path.join(rbasepath, urldir, render_outdir, '')
        render_url_imgpath = os.path.join(rbasepath, urldir, render_imgdir, '')
        return render_url_path, render_url_imgpath

def get_webrenderer_path2(cfgObj, urlflag=None):
        projectname = cfgObj.get_config('renderinfo', 'projectname').lstrip('/')
        renderurlbasepath = cfgObj.get_config('renderinfo', 'renderurlbasepath')
        renderbasepath = cfgObj.get_config('renderinfo', 'renderbasepath')
        rbasepath = renderurlbasepath if urlflag else renderbasepath
        rpath = os.path.join(rbasepath, projectname, 'data', 'output', '')
        return rpath

def get_render_dbconnstr(projectid, urlid, cfgObj):
        dbinfostr = cfgObj.get_config('database', 'dbconnstr')
        dbprefix = cfgObj.get_config('database', 'dbprefix')
        dbcommon = cfgObj.get_config('database', 'dbcommon')
        #dbname = '%s%s' %(str(dbprefix), str(urlid))
        dbname = '%s%s_%s' %(str(dbprefix), str(projectid), str(urlid))
        dbconnstr_url = '%s%s#' %(dbinfostr, dbname)
        dbconnstr_common = '%s%s#' %(dbinfostr, dbcommon)
        return dbconnstr_common, dbconnstr_url

def get_common_dbconnstr(cfgObj):
        dbinfostr = cfgObj.get_config('database', 'dbconnstr')
        dbcommon = cfgObj.get_config('database', 'dbcommon')
        dbconnstr_common = '%s%s#' %(dbinfostr, dbcommon)
        return dbconnstr_common

def get_urlid_dbconnstr(projectid, urlid, cfgObj):
        dbinfostr = cfgObj.get_config('database', 'dbconnstr')
        dbprefix = cfgObj.get_config('database', 'dbprefix')
        #dbname = '%s%s' %(str(dbprefix), str(urlid))
        dbname = '%s%s_%s' %(str(dbprefix), str(projectid), str(urlid))
        dbconnstr_url = '%s%s#' %(dbinfostr, dbname)
        return dbconnstr_url

