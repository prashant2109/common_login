from db.webdatastore import webdatastore
objdb = webdatastore()

class get_parent_child_relation(object):
    def __init__(self):
        pass

    def get_taxo_parent_order_dict(self, dbpath):             
        db_dict = objdb.read_all_from_lmdb(dbpath)
        header, data_list = db_dict.get('HEADERS', []), db_dict.get('ROWS', [])
        order_taxo_dict = {}
        display_index_dict = {}
        for each_row in data_list:
            display_index = float(each_row.get(1+header.index('DISPLAY_INDEX'), 0.0))
            tx_taxo_parent = each_row.get(1+header.index('TX_TAXO_PARENT'))
            tx_taxo = each_row.get(1+header.index('TX_TAXO'))
            selection_flg = each_row.get(1+header.index('SELECTION_FLAG'))
            derived_flg = each_row.get(1+header.index('DERIVED_DATA'))
            if derived_flg and int(derived_flg) == 1:continue  
            if selection_flg and int(selection_flg) == 0:continue
            if display_index == 0.0:continue
            new_display_index = str(display_index)
            new_display_index_lst = new_display_index.split('.')
            if not display_index_dict.get(tx_taxo_parent, {}):
                display_index_dict[tx_taxo_parent] = {}
            if not display_index_dict[tx_taxo_parent].get(new_display_index_lst[0], []):
                display_index_dict[tx_taxo_parent][new_display_index_lst[0]] = []
            if display_index not in display_index_dict[tx_taxo_parent][new_display_index_lst[0]]:display_index_dict[tx_taxo_parent][new_display_index_lst[0]].append(display_index) 
        for each_row in data_list:
            display_index = float(each_row.get(1+header.index('DISPLAY_INDEX'), 0.0))
            tx_taxo_parent = each_row.get(1+header.index('TX_TAXO_PARENT'))
            tx_taxo = each_row.get(1+header.index('TX_TAXO'))
            selection_flg = each_row.get(1+header.index('SELECTION_FLAG'))
            if selection_flg and int(selection_flg) == 0:continue
            if display_index == 0.0:continue
            derived_flg = each_row.get(1+header.index('DERIVED_DATA'))
            if derived_flg and int(derived_flg) == 1:continue  
            new_display_index = str(display_index)
            new_display_index_lst = new_display_index.split('.')
            key = (tx_taxo_parent, tx_taxo)
            if not order_taxo_dict.get(key, []):
                order_taxo_dict[key] = []    
            display_index_lst = display_index_dict.get(tx_taxo_parent, {}).get(new_display_index_lst[0], [])
            for each_val in display_index_lst: 
                if each_val not in order_taxo_dict[key]:
                    order_taxo_dict[key].append(each_val)
        return order_taxo_dict 
