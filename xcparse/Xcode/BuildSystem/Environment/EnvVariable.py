from .EnvVarCondition import *
from ....Helpers import logging_helper
import objc

class EnvVariable(object):
    
    def __init__(self, dictionary):
        if 'Name' in dictionary.keys():
            self.name = dictionary['Name'];
        self.Type = 'String'; # default for now
        if 'Type' in dictionary.keys():
            self.Type = dictionary['Type'];
        if 'DefaultValue' in dictionary.keys():
            self.DefaultValue = dictionary['DefaultValue'];
        else:
            default_values = {
                'Boolean': 'NO',
                'Bool': 'NO',
                'bool': 'NO',
                
                'String': '',
                'string': '',
                
                'Enumeration': '',
                'enum': '',
                
                'PathList': '',
                'pathlist': '',
                
                'Path': '',
                'path': '',
                
                'StringList': '',
                'stringlist': '',
            };
            
            if self.Type in default_values:
                self.DefaultValue = default_values[self.Type];
            else:
                logging_helper.getLogger().warning('[EnvVariable]: type not found %s' % (self.Type));
        self.values = set();
        self.mergeDefinition(dictionary);
    
    def __attrs(self):
        return (self.name, self.type);
    
    def __repr__(self):
        return '(%s : %s : %s : %s - %s)' % (type(self), self.name, self.Type, self.DefaultValue, self.values);
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name and self.Type == other.Type;
    
    def __hash__(self):
        return hash(self.__attrs());
    
    def isPath(self):
        return self.Type in ['path', 'Path', 'pathlist', 'PathList'];
    
    def isString(self):
        return self.Type in ['string', 'String', 'stringlist', 'StringList'];
    
    def isBoolean(self):
        return self.Type in ['Boolean', 'bool', 'Bool'];
    
    def isEnum(self):
        return self.Type in ['enum', 'Enumeration'];
    
    def mergeDefinition(self, dictionary):
        for key in dictionary.keys():
            if hasattr(self, key) == False:
                setattr(self, key, dictionary[key]);
            else:
                if dictionary[key] != getattr(self, key):
                    setattr(self, key, dictionary[key]);
    
    def addConditionalValue(self, conditional):
        if len(conditional.keys) == 0:
            self.DefaultValue = conditional.value;
        self.values.add(conditional);
    
    def value(self, environment):
        result_value = self.DefaultValue;
        for conditional in self.values:
            if conditional.evaluate(environment) == True:
                result_value = conditional.value;
                break;
        # add check for parsing the value if necessary
        if type(result_value) is unicode:
            result_value = str(result_value);
        if type(result_value) is objc.pyobjc_unicode:
            result_value = str(result_value);
        if type(result_value) is str:
            test_result_value = environment.parseKey(result_value);
            if test_result_value[0] == True:
                result_value = test_result_value[1];
        else:
            result_str = '';
            for item in result_value:
                result_str += str(item)+' ';
            result_value = result_str;
        if '$(inherited)' in result_value:
            # is this correct?
            result_value = result_value.replace('$(inherited)', ' ');
        return result_value;
    
    def commandLineFlag(self, environment):
        result = None;
        value = self.value(environment);
        if hasattr(self, 'CommandLineArgs') == True:
            if hasattr(self.CommandLineArgs, 'keys') and callable(getattr(self.CommandLineArgs, 'keys')):
                # this is checking allowed values to be passed and looked up
                # if hasattr(self, 'AllowedValues') == True and value in getattr(self, 'AllowedValues'):
                if value in self.CommandLineArgs.keys():
                    result = self.CommandLineArgs[value];
                    if type(result) == objc.pyobjc_unicode:
                        result = (result,);
                else:
                    if '<<otherwise>>' in self.CommandLineArgs.keys():
                        result = self.CommandLineArgs['<<otherwise>>'];
                    else:
                        logging_helper.getLogger().warn('[EnvVariable]: Could not look-up value "%s" in args dictionary "%s"' % (value, self.CommandLineArgs));
            else:
                result = self.CommandLineArgs;
        # change array to string
        if result != None:
            if len(result) > 0:
                result_str = '';
                for item in result:
                    result_str += str(item)+' ';
                result = result_str;
                if '$(value)' in result:
                    if len(value) == 0:
                        result = '';
                    else:
                        result = result.replace('$(value)', value);
                result = environment.parseKey(result)[1];
        return result;