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
            result = self.parseLine(line);
            for item in result:
                self.setValueForKey(item[0], item[1], item[2]);
        
        override_lines = [];
        if self.path != None and os.path.exists(self.path):
            override_lines = [line.strip() for line in open(self.path)];
        
    def parseLine(self, line):
        config = None;
        key = 'DEFAULT_KEY';
        value = 'DEFAULT_VALUE';
        configs = [];
        
        
        
        configs.append((config, key, value));
        
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