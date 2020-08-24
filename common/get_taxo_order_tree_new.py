import os, sys, copy
import MySQLdb
import ConfigParser
from db.webdatastore import webdatastore
objdb = webdatastore()

class GetTaxoTreeInfo():
    def __init__(self, cf):
        self.config_path = cf
        self.config = ConfigParser.ConfigParser()
        self.config.read(cf)
        self.dbpath = self.config.get('modeldb', 'value')        
        self.pc_dbpath = self.config.get('model_name_det', 'pc_db')

    def connection(self):
        data = self.config.get('database','value')
        khost, kpasswd, kuser, kdb = data.split('##')
        conn = MySQLdb.connect(khost, kuser, kpasswd, kdb)
        cur = conn.cursor()
        return cur, conn

    def get_agent_id_from_doc_id(self, doc_id):
        stmt = "select agent_id from document_master where document_id = %s" % (doc_id)
        cur, con = self.connection()
        cur.execute(stmt)
        res = cur.fetchone()
        con.close()
        if res:
            return res[0]
        else:
            return 0

  
    def get_proj_case_id_from_agent_id(self, agent_id):
        stmt = "select CaseID, ProjectID from batch_mgmt where agent_id  = %s" % (agent_id)
        cur, con = self.connection()
        cur.execute(stmt)
        res = cur.fetchone()
        con.close()
        if res:
           return res[0], res[1]
        else:
           return 0,0

    def get_all_assigned_txo_id_dict(self, case_proj_id_str):
        ret_dict = {}
        stmt = "select taxo_id, assign_taxonomy,taxonomy_type from taxonomy_mapping where project_id = '%s'" % (case_proj_id_str) 
        cur, con = self.connection()
        cur.execute(stmt)
        res = cur.fetchall()
        con.close()
        for each in res:
            taxo_id, assign_taxonomy, taxonomy_type  = each[0:3]
            taxo_id = int(taxo_id)
            if not taxo_id:continue
            if not ret_dict.get(taxo_id, None):
              ret_dict[taxo_id] = {'assign_taxonomy':assign_taxonomy, 'taxo_type':taxonomy_type} 
        return ret_dict
      
    def get_txo_id_level_dict(self, case_proj_id_str):
        ret_dict = {}
        node_id_parent_id_dict = {}
        stmt = "select node_id, node_name, parent_id, level_str from taxonomy_master where proj_id = '%s'" % (case_proj_id_str)
        #print stmt
        cur, con = self.connection()
        cur.execute(stmt)
        res = cur.fetchall()
        con.close()
        for each in res:
            node_id, node_name, parent_id, level_str  = each[0:4]
            node_id = int(node_id)
            parent_id = int(parent_id)
            if not node_id:continue
            if not ret_dict.get(node_id, None):
              node_id_parent_id_dict[node_id] = {'parent_id':parent_id, 'node_name':node_name}
              if parent_id: 
                  ret_dict[node_id] = {'level_str':level_str, 'node_name':node_name, 'parent_id':parent_id}
        return ret_dict, node_id_parent_id_dict

    def get_pc_dict(self, case_proj_id_str):
        ret_dict = {}
        root_nodes = []
        pc_dict = {}
        node_id_parent_id_dict = {}
        stmt = "select node_id, node_name, parent_id, level_str from taxonomy_master where proj_id = '%s'" % (case_proj_id_str)
        #print stmt
        cur, con = self.connection()
        cur.execute(stmt)
        res = cur.fetchall()
        con.close()
        node_level_dict = {}  
        for each in res:
            node_id, node_name, parent_id, level_str  = each[0:4]
            node_level_dict[node_id] = level_str
            #print node_id, node_name, parent_id, level_str
            node_id = int(node_id)
            parent_id = int(parent_id)
            if not node_id:continue
            if not pc_dict.get(node_id, []):
                pc_dict[node_id] = []
             
            if not pc_dict.get(parent_id, []):
                pc_dict[parent_id] = []
  
            pc_dict[parent_id].append(node_id)

            if not ret_dict.get(node_id, None):
               ret_dict[node_id] = {'level_str':level_str, 'node_name':node_name, 'parent_id':parent_id}
            #if len(level_str.split('.')) == 1:
            if parent_id == 0:
               root_nodes.append(node_id)
        for p, chs in pc_dict.items():
            if p == 0: continue
            mx = {} 
            for ch in chs:
                #print ch, ' ===A=== ', node_level_dict.get(ch, ''), '==== ', p
                x = node_level_dict.get(ch, '')
                mx[tuple(map(lambda x:int(x), x.split('.')))] = ch
            if mx:     
                f_mx = sorted(mx.keys(), key=lambda each:each[-1]) 
                #print 'AAAA', f_mx
                f_mx_lst = []
                for mm in f_mx:
                    f_mx_lst.append(mx[mm]) 
                #print f_mx_lst
                pc_dict[p] = f_mx_lst[:]

        return ret_dict, pc_dict, root_nodes

    def get_table_type(self, given_node_parent, node_id_parent_id_dict):
        table_type = ''
        total_parent_len = len(node_id_parent_id_dict.keys())
        cnt =  1
        while cnt <= total_parent_len:
            parent_id_dict = node_id_parent_id_dict.get(given_node_parent, {})
            if not parent_id_dict:
                break
            parent_id = parent_id_dict.get('parent_id', None)
            if parent_id == 0:
                table_type = parent_id_dict.get('node_name', '')
                break
            given_node_parent = parent_id
            cnt = cnt + 1
        return table_type 
        
    def get_tt_taxo_level_dict(self, taxo_id_level_dict, node_id_parent_id_dict):
        tt_taxo_level_dict, taxo_level_idex_dict = {}, {}
        taxo_ids = taxo_id_level_dict.keys()
        taxo_ids.sort()
        for index, taxo_id in enumerate(taxo_ids, 1):
            taxo_name_index_dict = taxo_id_level_dict[taxo_id]   
            taxonomy = taxo_name_index_dict['node_name']
            level_str = taxo_name_index_dict['level_str']
            parent_id = taxo_name_index_dict['parent_id']
            table_type = self.get_table_type(parent_id, node_id_parent_id_dict)
            if not table_type:continue
            if not tt_taxo_level_dict.get(table_type, None):
                tt_taxo_level_dict[table_type] = {}
                taxo_level_idex_dict[table_type] = {}
            tt_taxo_level_dict[table_type][taxonomy] = {'taxo_level': level_str, 'index':index}    
            taxo_level_idex_dict[table_type][level_str] = index
        #print tt_taxo_level_dict['BS']
        #sys.exit()
        return tt_taxo_level_dict, taxo_level_idex_dict    
 
    def get_taxo_tree(self, doc_id):
       agent_id = self.get_agent_id_from_doc_id(doc_id)
       case_id, proj_id = self.get_proj_case_id_from_agent_id(agent_id) 
       case_proj_id_str = "_".join([str(case_id), str(proj_id)])
       #assigned_taxo_id_dict = self.get_all_assigned_txo_id_dict(case_proj_id_str) 
       taxo_id_level_dict, node_id_parent_id_dict = self.get_txo_id_level_dict(case_proj_id_str) 
       tt_taxo_level_dict, taxo_level_idex_dict = self.get_tt_taxo_level_dict(taxo_id_level_dict, node_id_parent_id_dict)
       #print assigned_taxo_id_dict
       #print taxo_id_level_dict
       return tt_taxo_level_dict, taxo_level_idex_dict 

    def create_row_objects(self, taxo_level_idex_dict, pc_dict, root_nodes):
        row_map_dict = {}  
        for k, v in taxo_level_idex_dict.items():
            each_row = []
            each_cell = {}
            each_cell['node_name'] = v.get('node_name', '')
            each_cell['children'] = []
            each_row.append(each_cell) 
            row_map_dict[k] = copy.deepcopy(each_row)
        for root_node in root_nodes:
            each_row = []
            each_cell = {}
            each_cell['node_name'] = taxo_level_idex_dict.get(root_node, {}).get('node_name', '')
            each_cell['children'] = []
            each_row.append(each_cell)
            row_map_dict[root_node] = copy.deepcopy(each_row)
 
        return row_map_dict 

    def get_child_objs(self, node, row_map_dict, pc_dict, level):
        #if level >2: return row_map_dict, level
        chs = pc_dict.get(node, [])
        for ch in chs:
            ch_obj = row_map_dict[ch]
            row_map_dict[node][0]['children'] += ch_obj
            #print node, '=======', row_map_dict[node], ch_obj 
            row_map_dict, level = self.get_child_objs(ch, row_map_dict, pc_dict, level)
        level += 1 
        return row_map_dict, level

    def final_row_list(self, row_map_dict, pc_dict, root_nodes):

        def disp(node, row_map_dict):
            x = row_map_dict.get(node, [])
            for each_x in x:
                print len(each_x.get('children', '')), each_x['node_name']
                disp(each_x['node_name'], row_map_dict)

        final_rows =[]
        for root_node in root_nodes:
            level = 0  
            row_map_dict, level = self.get_child_objs(root_node, row_map_dict, pc_dict, level)
            #print root_node, ' ----- ', row_map_dict.get(root_node, [])
            disp(root_node, row_map_dict)
            final_rows.append(row_map_dict.get(root_node, [{}])[0])
            
        '''
        root_is_child_12 = [{'node_name':'IS11', 'children':[]}, {'node_name':'IS12', 'children':[]}, {'node_name':'IS13', 'children':[]}]
        root_is_child_22 = [{'node_name':'IS21', 'children':[]}, {'node_name':'IS22', 'children':[]}, {'node_name':'IS23', 'children':[]}]
        root_is_child_32 = [{'node_name':'IS31', 'children':[]}, {'node_name':'IS32', 'children':[]}, {'node_name':'IS33', 'children':[]}]
        root_is_child = [{'node_name':'IS1', 'children':root_is_child_12}, {'node_name':'IS2', 'children':root_is_child_22}, {'node_name':'IS3', 'children':root_is_child_32}]
        root_bs_child = [{'node_name':'BS1', 'children':[]}, {'node_name':'BS2', 'children':[]}, {'node_name':'BS3', 'children':[]}]
        root_cf_child = [{'node_name':'CF1', 'children':[]}, {'node_name':'CF2', 'children':[]}, {'node_name':'CF3', 'children':[]}]
        root_is = {'node_name':'IS', 'children':root_is_child}
        root_bs = {'node_name':'BS', 'children':root_bs_child}
        root_cf = {'node_name':'CF', 'children':root_cf_child}
        final_rows = [root_is,root_bs,root_cf] 
        '''
        print final_rows
        return final_rows

    def get_col_def(self):
        users_columnDefs    = [
                    #{'name':'node_name', "headerCellClass": "kve_header", "displayName": "Description", "cellClass": "grid-align_center", 'cellTemplate':'<div></div>'}
                    {'name':'node_name', "headerCellClass": "kve_header", "displayName": "Description", "cellClass": "grid-align_left"}
                      ]
        return users_columnDefs

    def read_taxo_tree(self, company_name):
        dbname = "{dbpath}/{company_name}/{pc_dbpath}".format(dbpath = self.dbpath, company_name = company_name, pc_dbpath = self.pc_dbpath)
        col_def = self.get_col_def()
        pc_dict = objdb.read_all_from_lmdb(dbname)
        comp_pc_dict = pc_dict.get('pc_dict', {}).get(company_name, [])
        return col_def, comp_pc_dict

    def get_taxo_tree_new(self, case_id, proj_id, company_name):
        pc_dict = {}
        dbname = "{dbpath}/{company_name}/{pc_dbpath}".format(dbpath = self.dbpath, company_name = company_name, pc_dbpath = self.pc_dbpath)
        col_def = self.get_col_def()
        case_proj_id_str = "_".join([str(case_id), str(proj_id)])
        taxo_id_level_dict, pc_dict, root_nodes = self.get_pc_dict(case_proj_id_str)
        row_map_dict = self.create_row_objects(taxo_id_level_dict, pc_dict, root_nodes)
        final_rows = self.final_row_list(row_map_dict, pc_dict, root_nodes)
        if not pc_dict.get(company_name, []):
            pc_dict[company_name] = []
        pc_dict[company_name] = final_rows
        pc_obj = {'pc_dict':pc_dict}
        objdb.write_to_lmdb(dbname, pc_obj, pc_obj.keys(), 1)
        return  col_def, final_rows
 
if __name__ == "__main__":
    config_path = '/root/Honnegowda/ModelBuilder_v2/pysrc/dbConfig.ini'
    obj = GetTaxoTreeInfo(config_path)
    doc_id = 4889 
    tt_taxo_level_dict, taxo_level_idex_dict = obj.get_taxo_tree(doc_id)
