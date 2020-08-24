
class datahandler(object):
    def __init__(self, header, rows):
        self._header = header[:]
        self._rows = rows[:]

    def add_column(self, colname):
        if colname not in self._header:
            self._header.append(colname)
            return 
        return 'Err:DUPLICATECOLUMN'  

    def __get_col_index(self, colname):
        if colname not in self._header:
            self._header.append(colname)
        idx = 1 + self._header.index(colname)
        return idx

    def get_value(self, row, colname):
        if colname not in self._header:
            return 'Err:COLNAME'
        #print self.__get_col_index(colname), row
        return row.get(self.__get_col_index(colname), '')

    def __check_cols(self, rowdata):
        return
 
    def add_row(self, rowdata):
        tmp_row = {}
        tmp_row[self.__get_col_index('ROWIDX')] = 1+len(self._rows)
        for colindex, data in rowdata.items():
            colname = self._header[colindex-1]
            if colname == 'ROWIDX':
                return 'Err:DUPLICATEROW'
            tmp_row = self.add_coldata(tmp_row, colname, data)
        self._rows.append(tmp_row)
 
    def add_coldata(self, rowdata, colname, data):
        rowdata[self.__get_col_index(colname)] = data
        return rowdata
 
    def update_coldata(self, rowdata, colname, data):
        mx = rowdata.get(self.__get_col_index(colname), None) 
        if mx:
            self.add_coldata(rowdata, colname, data)
            return
        return 'Err:DATAUPDATE'

    def get_datarows(self):
        datarows = []
        for row in self._rows:
            tmp = {}
            for rowidx, val in row.items():
                colname = self._header[rowidx-1]
                tmp[colname] = val
            datarows.append(tmp) 
        return datarows
 
    def get_index_value(self, row, colname):
        colidx = self.__get_col_index(colname)
        return row.get(colidx, '')

    def get_colname_value(self, row, colname):
        return row.get(colname, '')

    def debug_all_rows(self):
        for row in self._rows:
            self.debug_row(row)

    def debug_row(self, row):
        print 'o^o'*60
        for idx, colname in enumerate(self._header):
            if row.get(1+idx, ''):  
                print [colname, row[1+idx]], 
        print
 
    def return_data(self):
        return self._header, self._rows
   

if __name__=="__main__":
    obj = datahadler([], []) 
