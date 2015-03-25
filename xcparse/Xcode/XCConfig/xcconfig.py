import os
import sys
from ...Helpers import path_helper
from .xcconfig_line_resolver import *

class xcconfig(object):
    
    def __init__(self, path):
        self.path = path;
        self.lines = [];
        
        
        if self.path != None:
            config_lines = [];
            if os.path.exists(self.path):
                config_lines = [line.strip() for line in open(self.path)];
        
            for line in config_lines:
                line_type = xcconfig_line_type(line);
                type_constructor = xcconfig_line_resolver(line, line_type);
                if type_constructor[0] == True:
                    line_obj = type_constructor[1](line);
                    self.lines.append(line_obj);
    
    @classmethod
    def pathForBuiltinConfigWithName(self, name):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), name);
        
    
    # def valueForKey(self, config, key):
    #     if key in self.__build_settings.keys():
    #         return self.__build_settings[key].getValue(config);
    #     else:
    #         return None;
    #
    # def setValueForKey(self, config, key, value):
    #     if key in self.__build_settings.keys():
    #         self.__build_settings[key].setValue(config, value);
    #     else:
    #         new_kv = xcconfig_item((config, key, value));
    #         self.__build_settings[key] = new_kv;