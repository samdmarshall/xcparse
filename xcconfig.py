import os
import sys
import Path


class xcconfig(object):
    
    def __init__(self, path):
        self.defaults = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'defaults.xcconfig');
        self.path = path;
        
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
        key = '';
        value = '';
        configs = [];
        
        configs.append((config, key, value));
        
        return configs;
        
    def valueForKey(self, config, key):
        if config == '' or config == None:
            return self.__build_settings['defaults'][key];
        else:
            return self.__build_settings['Configuration'][config][key];
    
    def setValueForKey(self, config, key, value):
        if config == '' or config == None:
            self.__build_settings['defaults'][key] = value;
        else:
            self.__build_settings['Configurations'][config][key] = value;