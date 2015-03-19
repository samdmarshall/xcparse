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
            self.default_value = dictionary['DefaultValue'];
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
                self.default_value = default_values[self.type];
            else:
                logging_helper.getLogger().warning('[EnvVariable]: type not found %s' % (self.type));
        self.values = set();
    
    def __attrs(self):
        return (self.name, self.type);
    
    def __repr__(self):
        return '(%s : %s : %s)' % (type(self), self.name, self.type);
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name and self.type == other.type;
    
    def __hash__(self):
        return hash(self.__attrs());
    
    def addConditionalValue(self, conditional):
        if len(conditional.keys) == 0:
            self.default_value = conditional.value;
        self.values.add(conditional);
    
    def value(self, environment):
        result_value = self.default_value;
        for conditional in self.values:
            if conditional.evaluate(environment) == True:
                result_value = conditional.value;
                break;
        return result_value;