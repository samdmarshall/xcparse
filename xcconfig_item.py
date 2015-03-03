import os
import sys

class xcconfig_item(object):
    
    def __init__(self, item):
        self.key_name = item[2];
        self.default_value = '';
        self.lookup_value = {};
        
        
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
    