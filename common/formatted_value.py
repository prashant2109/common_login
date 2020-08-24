import os, sys 
 
class formatted_value: 
    def get_formatted_value(self, assump_val, displayType, displayFormat):
        assump_val = str(assump_val)
        if '.' in displayFormat:
            try:
                assump_val = float(assump_val)
                suffix_char = ''
                if '%' == displayFormat[-1]:
                    suffix_char = '%'
                    displayFormat = displayFormat[:-1] 
                    #assump_val = assump_val  * 100
                elif 'x' == displayFormat[-1]:
                    suffix_char = 'x'
                    displayFormat = displayFormat[:-1] 
                lst = displayFormat.split('.')
                decimal_val = len(lst[-1]) 
                assump_val = '{:,.{}f} {}'.format(assump_val, decimal_val, suffix_char)
            except:
                pass
        else:
            if '.' in str(assump_val):
                assump_val = assump_val.split('.')[0]
            try:
               assump_val = int(assump_val)
               suffix_char = ''
               if '%' == displayFormat[-1]:
                    suffix_char = '%'
                    displayFormat = displayFormat[:-1] 
                    #assump_val = assump_val  * 100
               elif 'x' == displayFormat[-1]:
                    suffix_char = 'x'
                    displayFormat = displayFormat[:-1]
               assump_val = '{:,}{}'.format(assump_val, suffix_char) 
            except:
                pass

        if '-' in str(assump_val):
            assum_val_lst = str(assump_val).split(' ')
            if len(assum_val_lst) > 1:
                assump_val = '(' + assum_val_lst[0].strip('-') + ') ' + assum_val_lst[-1]
            else:
                assump_val = '(' + assum_val_lst[0].strip('-') + ') '
        if assump_val == 'NA':
            assump_val = '-'
        #print "Formattteddd...: ",displayFormat, 'd: ', displayType, 'a: ',assump_val
        return assump_val

if __name__ == "__main__":
    obj = formatted_value()
    print obj.get_formatted_value('100', '', 'n.nn')
