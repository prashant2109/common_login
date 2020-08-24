def add_tt_missing_years(tt_ph_info_dict, derived_flag=0):
    all_ph_li = []
    for tt, ph_dict in tt_ph_info_dict.items():
        ph_li = ph_dict.keys()
        for ph_year in ph_li:
            ph_label = ph_year[0:2]
            if ph_year not in all_ph_li:
                if((ph_label in ['Q4', 'H2']) and (not derived_flag)):
                    continue
                all_ph_li.append(ph_year)

    for tt, ph_year_dict in tt_ph_info_dict.items():
        tt_year_li = ph_year_dict.keys()
        add_year_li = list(set(all_ph_li) - set(tt_year_li))
        for each_year in add_year_li:
           ph_year_dict[each_year] = (each_year, '', 'AUDITED')
    return tt_ph_info_dict

