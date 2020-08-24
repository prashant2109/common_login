# -*- coding: utf-8 -*-
import os, sys
import ConfigParser
import report_year_sort as report_year_sort


class ValidateTabletypePh(object):
    def __init__(self, cf):
        self.config_path = cf
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.config_path)
        self.data_path = self.config.get('data_path', 'value')
        self.rule_dict = {}
        self.get_rule_id_dict()

    def get_rule_id_dict(self):
        fname = 'table_type_ph_validation_rules.txt'
        fname_path = os.path.join(self.data_path, fname)
        if os.path.exists(fname_path):
            fin = open(fname_path) 
            rule_li = [each.strip().split() for each in fin.readlines()]
            for each_rule in rule_li:
                rule_id, table_type, cur_year, pre_year = each_rule
                if not self.rule_dict.get(table_type, None):
                   self.rule_dict[table_type] = {}
                self.rule_dict[table_type][rule_id] = {}
                self.rule_dict[table_type][rule_id]['cur_year'] = cur_year
                self.rule_dict[table_type][rule_id]['prev_year'] = pre_year
        return
    
    def validate_years(self, table_type, ph_list):
        rule_ids = self.rule_dict.get(table_type, {}).keys()
        if not rule_ids:
            return True
        ph_li = report_year_sort.year_sort(ph_list)
        curr_year = ph_li[-1]
        curr_year_lable = curr_year[:-4]
        res_list = []
        for each_year in ph_li[:-1]:
            prev_year_label = each_year[:-4]
            for rid in rule_ids:
                cur_year = self.rule_dict[table_type][rid]['cur_year']
                pre_year = self.rule_dict[table_type][rid]['prev_year']
                if cur_year == curr_year_lable and pre_year == prev_year_label:
                    res_list.append(each_year)

        if res_list == ph_li[:-1]:
            return True
        return False


    def validate_tabletype_ph_rules(self, tt_wise_ph_li):
        tt_rule_error_dict = {}
        for tt, ph_li in tt_wise_ph_li.iteritems():
            flag = self.validate_years(tt, ph_li)
            if not flag:
                tt_rule_error_dict[tt] = ph_li
        return tt_rule_error_dict

    def validate_tabletype_ph_rules_old(self, tt_wise_ph_li):
        tt_rule_error_dict = {}
        for tt, ph_li in tt_wise_ph_li.iteritems():
            tt_rule_dict = self.tt_rule_id_dict.get(tt, {})
            if tt_rule_dict:
                ph_li = report_year_sort.year_sort(ph_li)
                recent_year = ph_li[-1]
                recent_year_lbl =  recent_year[:-4]
                for each_prev_year in ph_li[::-1][1:]:
                    prev_year_lbl = each_prev_year[:-4]
                    for rule_id, rule_dict in tt_rule_dict.iteritems():
                         
                        excpected_cur_year_lbl, excpected_prev_year_lbl =  rule_dict['cur_year_label'], rule_dict['prev_year_label']
                        if excpected_cur_year_lbl == recent_year_lbl:
                                if prev_year_lbl != excpected_prev_year_lbl:
                                    if not tt_rule_error_dict.get(tt, None):
                                        tt_rule_error_dict[tt] = {}
                                    tt_rule_error_dict[tt][rule_id] = {'cur_year_label':recent_year_lbl, 'expected_prev_year_lbl':excpected_prev_year_lbl, 'given_prev_year_labl':prev_year_lbl}    
                
        return tt_rule_error_dict                            

if __name__ == "__main__":
    cf = '/root/Honnegowda/ModelBuilder/ModelBuilder_v2/pysrc/dbConfig.ini'
    obj = ValidateTabletypePh(cf)
    #print obj.tt_rule_id_dict 
    tt_ph_li_dict = {'IS':['FY2015', 'FY2014'], 'CF':['FY2015','FY2015'], 'BS':['Q12015', 'Q12014']}
    tt_ph_li_dict = {'IS':['FY2015', 'FY2014'], 'CF':['FY2015','FY2015'], 'BS':['Q12015', 'FY2014']}
    tt_ph_li_dict = {'IS':['Q12015', 'FY2014'], 'CF':['Q12015','Q12015'], 'BS':['Q12015', 'Q12014']}
    tt_error_dict = obj.validate_tabletype_ph_rules(tt_ph_li_dict)
    print tt_error_dict
