from .EnvVarCondition import *
from .EnvVariable import *


def ParseKey(key_string, environment):
    string_length = len(key_string);
    offset = 0;
    
    while offset < string_length:
        find_sub = key_string.find('$');
        offset = find_sub;
    

class Environment(object):
    
    def __init__(self):
        self.settings = {};
    
    def addSetting(self, setting_dict):
        self.settings[setting_dict['Name']] = EnvVariable(setting_dict);
    
    def setValueForKey(self, key, value, condition_dict):
        result = self.settings[key];
        if result != None:
            result.addConditionalValue(EnvVarCondition(condition_dict, value));
    
    def valueForKey(self, key):
        value = None;
        result = self.settings[key];
        if result != None:
            value = result.value(self);
        return value;