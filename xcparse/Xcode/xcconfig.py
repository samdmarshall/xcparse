import os
import sys
from ..Helpers import path_helper

from .xcconfig_item import *

class xcconfig(object):
    
    def __init__(self, path):
        #self.defaults = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'defaults.xcconfig');
        self.path = path;
        self.__build_settings = {};
        
        # default_lines = [];
        # if os.path.exists(self.defaults):
        #     default_lines = [line.strip() for line in open(self.defaults)];
        # else:
        #     print 'Error in parsing defaults.xcconfig!';
        #     sys.exit(0);
        #
        # for line in default_lines:
        #     results = filter(lambda item: item[0] == True, self.parseLine(line));
        #     for item in results:
        #         self.setValueForKey(item[1], item[2], item[3]);
        
        override_lines = [];
        if self.path != None and os.path.exists(self.path):
            override_lines = [line.strip() for line in open(self.path)];
        
        for line in override_lines:
            results = filter(lambda item: item[0] == True, self.parseLine(line));
            for item in results:
                self.setValueForKey(item[1], item[2], item[3]);
        
        
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