import os
import sys

class xcenvironment_variable(object):
    
    def __init__(self, dictionary):
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
                print 'type not found %s' % (self.type);
        
        
    def value(self, environment):
        return self.default;