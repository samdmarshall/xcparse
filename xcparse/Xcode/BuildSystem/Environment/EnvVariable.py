from .EnvVarCondition import *
from ....Helpers import logging_helper

class EnvVariable(object):
    
    def __init__(self, dictionary):
        self.type = 'String'; # default for now
        if 'Name' in dictionary.keys():
            self.name = dictionary['Name'];
        if 'Type' in dictionary.keys():
            self.type = dictionary['Type'];
        if 'DefaultValue' in dictionary.keys():
            self.default = dictionary['DefaultValue'];
        else:
            default_values = {
                'Boolean': 'NO',
                'Bool': 'NO',
                'PathList': '',
                'String': '',
                'Enumeration': '',
                'stringlist': '',
                'Path': '',
                'StringList': '',
            };
            
            if self.type in default_values:
                self.default = default_values[self.type];
            else:
                logging_helper.getLogger().warning('[EnvVariable]: type not found %s' % (self.type));
        self.values = set();
        
        
    def addConditionalValue(self, conditional):
        self.values.union(set([conditional]));
    
    def value(self, environment):
        value = self.default;
        for conditional in self.values:
            if conditional.evaluate(environment) == True:
                value = conditional.value;
                break;
        return value;