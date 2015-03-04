import os
import sys
import Path

from .xcconfig_item import *

class xcconfig(object):
    
    def __init__(self, path):
        self.defaults = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'defaults.xcconfig');
        self.path = path;
        self.__build_settings = {};
        
        default_lines = [];
        if os.path.exists(self.defaults):
            default_lines = [line.strip() for line in open(self.defaults)];
        else:
            print 'Error in parsing defaults.xcconfig!';
            sys.exit(0);
        
        for line in default_lines:
            results = filter(lambda item: item[0] == True, self.parseLine(line));
            for item in results:
                self.setValueForKey(item[1], item[2], item[3]);
        
        override_lines = [];
        if self.path != None and os.path.exists(self.path):
            override_lines = [line.strip() for line in open(self.path)];
        
    def parseLine(self, line):
        result = False;
        config = None;
        key = 'DEFAULT_KEY';
        value = 'DEFAULT_VALUE';
        configs = [];
        
        # this needs to change over to use xcspec
        
        if line.startswith('//') == True:
            # comment
            configs.append((result, config, key, value));
        elif line.startswith('#include "') == True:
            # this needs to change item type to handle includes
            
            # parse include
            double_quote = line.find('"');
            
        else:
            # parse variable
            first_equals = line.find('=');
            first_bracket = line.find('[');
            #if first_bracket < first_equals:
                # 
        
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