import os
import sys

class xcconfig_item(object):
    
    def __init__(self, item):
        self.key_name = item[1];
        self.lookup_value = {};
        config = item[0];
        if config == None:
            self.default_value = item[2];
        else:
            self.default_value = '';
            condition_flavour = config[0];
            condition_value = config[1];
            self.lookup_value[condition_flavour][condition_value] = item[2];
        
        
    def getValue(self, config):
        if config != None:
            if config in self.lookup_value.keys():
                return self.lookup_value[config];
        return self.default_value;
    
    def setValue(self, config, value):
        if config != None:
            self.lookup_value[config] = value;
        else:
            self.default_value = value;
    