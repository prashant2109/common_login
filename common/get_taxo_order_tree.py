# -*- coding: utf-8 -*-
import xlsxReader as xlsxReader
xlr_obj = xlsxReader.xlsxReader()

def read_taxo_index_dict(data_path, xlsx_name):
    ret_dict = {}
    taxo_level_idex_dict = {}
    sheet_row_list_dict = xlr_obj.process(data_path, xlsx_name) 
    row_list = sheet_row_list_dict['Sheet1']
    if not row_list: return ret_dict
    for index, row in enumerate(row_list[1:], 1):
        table_type, taxo_level, taxonomy = row[0], row[1], row[2]
        if (not table_type) or (not taxonomy): continue
        if not ret_dict.get(table_type, {}):
            ret_dict[table_type] = {}
        if not taxo_level_idex_dict.get(table_type, {}):
            taxo_level_idex_dict[table_type] = {}
        ret_dict[table_type][taxonomy] = {'taxo_level': taxo_level, 'index':index}
        taxo_level_idex_dict[table_type][taxo_level] = index
    return ret_dict, taxo_level_idex_dict


