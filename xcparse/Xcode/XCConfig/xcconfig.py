import os
import sys
from ...Helpers import path_helper
from .xcconfig_line_resolver import *

class xcconfig(object):
    
    def __init__(self, path):
        self.path = path;
        self.kv = [];
        
        if self.path == None:
            self.path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'defaults.xcconfig');
        
        config_lines = [];
        if os.path.exists(self.path):
            config_lines = [line.strip() for line in open(self.path)];
        
        for line in config_lines:
            line_type = xcconfig_line_type(line);
            type_constructor = xcconfig_line_resolver(line, line_type);
            if type_constructor[0] == True:
                line_obj = type_constructor[1](line);
                self.kv.append(line_obj);
        
        
    def parseLine(self, line):
        config = None;
        key = 'DEFAULT_KEY';
        value = 'DEFAULT_VALUE';
        configs = [];
        
        offset = 0;
        # this needs to change over to use xcspec
        
        if line.startswith('//') == True:
            # comment
            configs.append((False, config, key, value));
        elif line.startswith('#include "') == True:
            # this needs to change item type to handle includes
            
            # parse include
            double_quote = line.find('"');
            
        else:
            curr = line[offset:];
            # parse variable
            find_equals = curr.find('=');
            find_open_bracket = curr.find('[');
            find_comment = curr.find('//');
            
            # this needs some error checking on line parsing
            
            if find_open_bracket == -1:
                # no conditional
                key = line[offset:find_equals].strip(' ');
                offset = find_equals + 1;
                if find_comment == -1:
                    value = line[offset:];
                else:
                    value = line[offset:find_comment];
                configs.append((True, config, key, value));
            else:
                # conditional value
                
                # while loop
                
                find_close_bracket =  curr.find(']');
                condition_name = line[find_open_bracket+1:find_equals];
                condition_value = line[find_equals+1:find_close_bracket];
                configs.append((False, (condition_name, condition_value), key, value));
        
        return configs;
        
    def valueForKey(self, config, key):
        if key in self.__build_settings.keys():
            return self.__build_settings[key].getValue(config);
        else:
            return None;
    
    def setValueForKey(self, config, key, value):
        if key in self.__build_settings.keys():
            self.__build_settings[key].setValue(config, value);
        else:
            new_kv = xcconfig_item((config, key, value));
            self.__build_settings[key] = new_kv;