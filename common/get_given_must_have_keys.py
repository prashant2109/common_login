import ConfigParser
import os

config = ConfigParser.ConfigParser()

class GetGivenDictMustHaveKeys(object):
    def __init__(self, cfgfile):
        config.read(cfgfile)
        self.data_path = config.get('data_path', 'value') 
 
    def get_given_dict_must_have_keys(self):
        fname = os.path.join(self.data_path, "given_dict_must_have_keys.txt")
        with open(fname, 'r') as fin:
            return [each.strip() for each in fin.readlines()]
