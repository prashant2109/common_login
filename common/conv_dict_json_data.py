def get_conv_dict_json_data(dictionary):

        def get_pp_dict(key, mdict, pp_dict):
            val = mdict[list(key)[-1]]
            if isinstance(val, dict):
                pp_dict[key] = val.keys()                 
                for each in val.keys():
                    pp_dict[tuple(list(key)+[each])] = []
                    get_pp_dict(tuple(list(key)+[each]), val, pp_dict)
        import copy 

        root_keys = []
        pp_dict = {}
        all_keys = dictionary.keys()
        for each in all_keys:
            pp_dict[('',each)] = []
            root_keys.append(('',each))
            get_pp_dict(('',each), dictionary, pp_dict)

        for k, v in pp_dict.items():
            #print k, v
            d = dictionary
            for x in list(k):
                if not x: continue
                if isinstance(x, tuple):
                    if not d.get('##'.join(map(lambda x:str(x),list(x)))):
                         d['##'.join(map(lambda x:str(x), list(x)))] = copy.deepcopy(d[x])
                         del d[x]
                elif d.get(x):
                    d = d[x]   
 
        return dictionary

        '''
        def update_dict(key, pp_dict, dictionary):
            print '__________________________________________'
            print key  
            for x in list(key):
                if not x: continue
                if isinstance(x, tuple):
                    if not d.get('##'.join(list(x))):
                         d['##'.join(list(x))] = copy.deep_copy(d[x])
                         del d[x]
                else:
                    print key, x, d.keys()
                    d = d[x]
                    if isinstance(d, dict):
                       print 'DICT : \t', d.keys()
                    else:
                       print 'DATA : \t', d
            print '_______________________________BREAK_________________________' 
            for k in pp_dict[key]:
                update_dict(tuple(list(key)+[k]), pp_dict, dictionary) 

            
        res_dict = {}
        for key in root_keys:
            update_dict(key, pp_dict, dictionary)
        '''
              




        '''
        def recc_dict(key, mdict):
            mkey = key
            val = mdict[key]
            if isinstance(val, list):
                new_val = []
                for each_val in val:
                    if isinstance(each_val, tuple):
                        new_val.append(list(each_val))
                    else:
                        new_val.append(each_val)   
                val = new_val[:]
            if isinstance(mkey, int):
                mkey = str(key)
            elif isinstance(mkey, tuple):
                mkey = '##'.join(list(key))
 
            if isinstance(val, dict):
                all_keys = val.keys() 
                for each in all_keys:
                    recc_dict(each, val) 
              
            mdict[mkey] = val
            #print mkey, type(mkey),  type(val)

        all_keys = dictionary.keys()
        for each in all_keys:
            recc_dict(each, dictionary)  
        '''

        def recc_disp(key, mdict):
            val = mdict[key]
            if isinstance(val, dict):
                all_keys = val.keys() 
                for each in all_keys:
                    recc_disp(each, val)
            print key, val  
 
        all_keys = dictionary.keys()
        for each in all_keys:
            recc_disp(each, dictionary)  
 
 
        return dictionary
        '''  
        for key, value in dictionary.iteritems():
            if type(key) == tuple:
                k = '##'.join(list(key))
                knew_dict[k] = value
                if isinstance(value, dict): 
                    print key, k
                    self.get_key_data_dict(value,knew_dict)
            elif type(key) == int:
                knew_dict[str(key)] = value
            else:
                knew_dict[key] = value

            if isinstance(value, dict):
                print key
                self.get_key_data_dict(value,knew_dict)
        '''  
