import os, sys
import os.path
import shelve
import ConfigParser
import glob
import dbcrypt
import datastore

class get_doc_data(object):
    def __init__(self, ipath, opath, isdb, isenc):
        self.__ipath = ipath
        self.__opath = opath
        self.__isdb = isdb
        self.__isenc = isenc
        return

    def __load_config(self, cfg_file):
        cfgObj = ConfigParser.SafeConfigParser()
        if not os.path.isfile(cfg_file):
            raise '%s, config file not found...' %(cfg_file)
        cfgObj.read(cfg_file)
        return cfgObj

    def write_to_shelve(self, fname, data):
        dirname = os.path.dirname(fname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        sh = shelve.open(fname)
        sh['data'] = data
        sh.close()
        return

    def read_from_shelve(self, fname, default=None):
        data = {}
        sh = shelve.open(fname)
        if sh:
            data = sh.get('data', default)
        sh.close()
        return data

    def write_to_db(self, dbname, idata, tabname):
        obj = dbcrypt.DBCrypt(self.__isenc)
        obj.write_to_dbcrypt(dbname, idata, tabname)
        return

    def read_from_db(self, dbname, tabname):
        obj = dbcrypt.DBCrypt(self.__isenc)
        data = obj.read_from_dbcrypt(dbname, tabname)
        return data

    def get_config(self, section, name):
        val = self.__cfgObj.get(section, name)
        if val:
            return val.strip()
        return None


    def get_xml_filenames(self, ipath, docid):
        xmlfilelst = glob.glob(os.path.join(ipath, docid, 'xml', '*.xml'))
        if not xmlfilelst:
            xmlfilelst = glob.glob(os.path.join(ipath, docid, 'xml', '*.db'))
        return xmlfilelst

    def get_pagenos(self, docid):
        pagenolst = []
        xmlfnames = self.get_xml_filenames(self.__ipath, docid)
        for xmlfname in xmlfnames:
            head, page_fname = os.path.split(xmlfname)
            pno = page_fname.split('.')[0]
            pagenolst.append(int(pno))
        pagenolst.sort()
        return pagenolst

    def getpagenos_db(self, docid, dirpath):
        dirname = os.path.join(dirpath, docid, 'db')
        pagenolst = os.listdir(dirname)
        pagenolst = [int(each) for each in pagenolst]
        pagenolst.sort()
        return pagenolst

    def get_page_nos(self, docid, isdb=0):
        pagenolst = []
        fnamelst = []
        if not isdb:
            pagenolst = self.get_pagenos(docid)
        else:
            pagenolst = self.getpagenos_db(docid, self.__ipath)
        pagenolst.sort()
        return pagenolst


    def get_pages(self, docid):
        pagenolst = []
        #ipath = self.get_config('project_input', 'ipath')
        ipath = self.__ipath[:]

        #dirname = os.path.join(ipath, docid)
        dirname = os.path.join(ipath, docid, 'db')

        pagenolst = os.listdir(dirname)
        pagenolst = [int(each) for each in pagenolst]
        pagenolst.sort()
        #print pagenolst

        return pagenolst

    def get_intersection_OLD(self, refbbox, bboxlst):
        retlst = []
        for bbox in bboxlst:
            if ( ((bbox[0] <= refbbox[2]) and (bbox[2] > refbbox[0])) or ((bbox[0] <= refbbox[0]) and (bbox[2] > refbbox[0])) ):
                if ( ((bbox[1] <= refbbox[3]) and (bbox[3] > refbbox[1])) or ((bbox[1] <= refbbox[1]) and (bbox[3] > refbbox[1])) ):
                    retlst.append(bbox)
        return retlst

    def get_intersection(self, refbbox, bboxlst):
        retlst = []
        for bbox in bboxlst:
            if ( ((bbox[0] <= refbbox[2]) and (bbox[2] > refbbox[0])) ):
                if ( ((bbox[1] <= refbbox[3]) and (bbox[3] > refbbox[1])) ):
                    retlst.append(bbox)
        return retlst

    def get_doc_data_old(self, docid, pno):
        ipath = self.__ipath[:]

        #fname = os.path.join(ipath, docid, str(pno), 'shelve', '%s.shv' %(str(pno)))
        #data = self.read_from_shelve(fname)

        tabname = 'pdfdata'
        fname = os.path.join(ipath, docid, 'db', str(pno), '%s.db' %tabname)
        data = self.read_from_db(fname, tabname)

        print data.keys()

        xmlid2chunkid = {}
        bbox2chunkid = {}
        chunkid2xmlid = {}
        chunkid2text = {}
        chunkid2bbox = {}

        chunk_dict = data.get('chunk_dict', {})
        for chunkid, tmpd in chunk_dict.items():
            xmlid = tmpd.get('xmlid', '')
            text = tmpd.get('text', '')
            bboxdict = tmpd.get('bbox', {})
            bbox = (bboxdict.get('x0', 0), bboxdict.get('y0', 0), bboxdict.get('x1', 0), bboxdict.get('y1', 0))

            xmlid2chunkid[xmlid] = chunkid
            bbox2chunkid[bbox] = chunkid
            chunkid2xmlid[chunkid] = xmlid
            chunkid2text[chunkid] = text
            chunkid2bbox[chunkid] = bbox

        return xmlid2chunkid, bbox2chunkid, chunkid2xmlid, chunkid2text, chunkid2bbox, chunk_dict

    def get_doc_data(self, docid, pno):
        ipath = self.__ipath[:]
	print 'JJJJJJJJJJJJJJJJJJJJ'

        #docdatafname = os.path.join(self.__opath, str(docid), 'get_doc_data', '%s.sh'%str(pno))
            
        docdatafname = os.path.join(self.__opath, str(docid), 'GDD', '%s.sh'%str(pno))
#        if os.path.isfile(docdatafname):
#	    print 'KKKK ', docdatafname
	    #commented temporarily to add wordspaces
            #print "innn"  
 #           return datastore.read_data_fname(docdatafname, self.__isdb, self.__isenc)
	#print 'JJJJJJJJJJJJJJJJJJJJ'
        tabname = 'pdfdata'
        ext = 'db' if self.__isdb else 'sh'
        fname = datastore.get_file_name(ipath, docid, pno, '%s.%s' %(tabname, ext), self.__isdb)
        #fname = os.path.join(ipath, docid, 'db', str(pno), '%s.db' %tabname)

        #print 'fname:', fname

        data = {}
        if self.__isdb:
            data = datastore.read_from_db_fname(fname, tabname, self.__isenc, {})
        else:
            data = datastore.read_from_shelve_fname(fname, {})
        #print '*********DDDDD***********', data.get('chunk_dict', {})
        #sys.exit()

        # font info
        font_data_dict = data.get('font_info', {})


        xmlid2chunkid = {}
        bbox2chunkid = {}
        chunkid2xmlid = {}
        chunkid2text = {}
        chunkid2bbox = {}

        chunk_dict = data.get('chunk_dict', {})
	
         
        for chunkid, tmpd in chunk_dict.items():
            xmlid = tmpd.get('xmlid', '')
            text = tmpd.get('text', '')
            bboxdict = tmpd.get('bbox', {})
            bbox = (bboxdict.get('x0', 0), bboxdict.get('y0', 0), bboxdict.get('x1', 0), bboxdict.get('y1', 0))

            xmlid2chunkid[xmlid] = chunkid
            bbox2chunkid[bbox] = chunkid
            chunkid2xmlid[chunkid] = xmlid
            chunkid2text[chunkid] = text
            chunkid2bbox[chunkid] = bbox

        # write data
        d = xmlid2chunkid, bbox2chunkid, chunkid2xmlid, chunkid2text, chunkid2bbox, chunk_dict, font_data_dict
        datastore.write_data_fname(docdatafname, self.__isdb, self.__isenc, d)
        print "innn"  
        return xmlid2chunkid, bbox2chunkid, chunkid2xmlid, chunkid2text, chunkid2bbox, chunk_dict, font_data_dict

    def get_all_pages_doc_data(self, docid):

        #docdatafname = os.path.join(self.__opath, str(docid), 'get_doc_data', 'docdata_%s.sh'%str(docid))
        docdatafname = os.path.join(self.__opath, str(docid), 'GDD', 'gdd_%s.sh'%str(docid))
        #if os.path.isfile(docdatafname):
         #   return datastore.read_data_fname(docdatafname, self.__isdb, self.__isenc)


        pagenolst = self.get_page_nos(docid, self.__isdb)

        xmlid2chunkid = {}
        bbox2chunkid = {}
        chunkid2xmlid = {}
        chunkid2text = {}
        chunkid2bbox = {}

        font_data_dict = {}
        chunk_dict = {}
        for pno in pagenolst:
            tmp_xmlid2chunkid, tmp_bbox2chunkid, tmp_chunkid2xmlid, tmp_chunkid2text, tmp_chunkid2bbox, tmp_chunk_dict, tmp_font_data_dict = self.get_doc_data(docid, pno)
            for k, v in tmp_xmlid2chunkid.items():
                xmlid2chunkid[k] = v
            for k, v in tmp_bbox2chunkid.items():
                bbox2chunkid[k] = v
            for k, v in tmp_chunkid2xmlid.items():
                chunkid2xmlid[k] = v
            for k, v in tmp_chunkid2text.items():
                chunkid2text[k] = v
            for k, v in tmp_chunkid2bbox.items():
                chunkid2bbox[k] = v

            #for k, v in tmp_chunk_dict.items():
            #    chunk_dict[k] = v
            #for k, v in tmp_font_data_dict.items():
            #    font_data_dict[k] = v

        # write data
        d = pagenolst, xmlid2chunkid, bbox2chunkid, chunkid2xmlid, chunkid2text, chunkid2bbox, chunk_dict, font_data_dict
        datastore.write_data_fname(docdatafname, self.__isdb, self.__isenc, d)
         
        return pagenolst, xmlid2chunkid, bbox2chunkid, chunkid2xmlid, chunkid2text, chunkid2bbox, chunk_dict, font_data_dict

    def debug(self):
        return

if __name__=='__main__':
    docid = sys.argv[1]
    obj = get_doc_data()
    obj.get_doc_data(docid, 1)

