from .EnvVarCondition import *
from .EnvVariable import *
from ...XCConfig.xcconfig import *

def ParseKey(key_string, environment):
    string_length = len(key_string);
    offset = 0;
    
    while offset < string_length:
        find_sub = key_string.find('$');
        offset = find_sub;
    

class Environment(object):
    
    def __init__(self):
        self.settings = {};
        # load default environment types
        
        # setting up default environment
        self.applyConfig(xcconfig(None));
    
    def addSetting(self, setting_dict):
        self.settings[setting_dict['Name']] = EnvVariable(setting_dict);
    
    def applyConfig(self, config_obj):
        for line in config_obj.lines:
            if line.type == 'KV':
                self.setValueForKey(line.key(), line.value(None), line.conditions());
            if line.type == 'COMMENT':
                # ignore this type of line
                continue;
            if line.type == 'INCLUDE':
                base_path = os.path.dirname(config_obj.path);
                path = line.includePath(base_path);
                self.applyConfig(xcconfig(path));
    
    def setValueForKey(self, key, value, condition_dict):
        if key in self.settings.keys():
            result = self.settings[key];
            if result != None:
                result.addConditionalValue(EnvVarCondition(condition_dict, value));
        else:
            print 'add value!';
    
    def valueForKey(self, key):
        value = None;
        if key in self.settings.keys():
            result = self.settings[key];
            if result != None:
                value = result.value(self);
        return value;