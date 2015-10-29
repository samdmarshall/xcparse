from .EnvVarCondition import *
from ....Helpers import logging_helper
from ....Helpers.pbPlist import pbItem
import objc
import re
from .EnvConstants import *


class EnvVariable(object):
    
    def __init__(self, dictionary):
        self.added_after = False;
        self.mergedKeys = set();
        self.parentValue = None;
        if 'Name' in dictionary.keys():
            self.name = dictionary['Name'];
        if self.name in kENVIRONMENT_LOOKUP.keys():
            self.Type = kENVIRONMENT_LOOKUP[self.name];
        else:
            self.Type = 'String'; # unknown default for now
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
    
    def __repr__(self):
        return '(%s : %s : %s : %s - %s)' % (type(self), self.name, self.Type, self.DefaultValue, self.values);
    
    def inheritedValue(self):
        return self.parentValue;
    
    def isList(self):
        return self.Type in ['stringlist', 'StringList', 'pathlist', 'PathList'];
    
    def isPath(self):
        return self.Type in ['path', 'Path', 'pathlist', 'PathList'];
    
    def isString(self):
        return self.Type in ['string', 'String', 'stringlist', 'StringList'];
    
    def isBoolean(self):
        return self.Type in ['Boolean', 'bool', 'Bool'];
    
    def isEnum(self):
        return self.Type in ['enum', 'Enumeration'];
    
    def mergeDefinition(self, dictionary, aggressive=True):
        self.added_after = True;
        for key in dictionary.keys():
            if type(key) is pbItem.pbString or type(key) is pbItem.pbQString:
                key = key.value
            if hasattr(self, key) == False:
                self.mergedKeys.add(key);
                setattr(self, key, dictionary[key]);
            else:
                if dictionary[key] != getattr(self, key) and aggressive == True:
                    setattr(self, key, dictionary[key]);
    
    def removeDefinition(self, dictionary, aggressive=True):
        self.added_after = False;
        for key in dictionary.keys():
            key = str(key)
            if hasattr(self, key) == True:
                if key in self.mergedKeys:
                    delattr(self, key);
                    self.mergedKeys.remove(key);
    
    def addConditionalValue(self, conditional):
        if len(conditional.keys) == 0:
            self.DefaultValue = conditional.value;
        self.values.add(conditional);
    
    def satisfiesCondition(self, environment, lookup_dict=None):
        if lookup_dict == None:
            lookup_dict = environment.resolvedValues();
        
        if hasattr(self, 'Condition') == True:
            expr = environment.parseKey(None, self.Condition, lookup_dict=lookup_dict)[1]
            expression = re.sub(' +',' ',str(expr))
            expression_list = expression.split(' ');
            list_filter_yes = map(lambda item: 'True' if item == 'YES' else item, expression_list);
            list_filter_no = map(lambda item: 'False' if item == 'NO' else item, list_filter_yes);
            list_filter_not = map(lambda item: 'not' if item == '!' else item, list_filter_no);
            list_filter_and = map(lambda item: 'and' if item == '&&' else item, list_filter_not);
            list_filter_or = map(lambda item: 'or' if item == '||' else item, list_filter_and);
            list_filter_strings = map(lambda item: '"'+item+'"' if item not in ['True', 'False', 'not', 'and', 'or', '==', '!=', '(', ')'] and not item.startswith('\\"') else item, list_filter_or);
            eval_string = ' '.join(list_filter_strings).replace('\\"', '"');
            return eval(eval_string);
        else:
            return True;
    
    def value(self, environment, lookup_dict=None):
        if lookup_dict == None:
            lookup_dict = environment.resolvedValues();
            
        result_value = self.DefaultValue;
        for conditional in self.values:
            if conditional.evaluate(environment, lookup_dict=lookup_dict) == True:
                result_value = conditional.value;
                break;
        # add check for parsing the value if necessary
        if type(result_value) is pbItem.pbString or type(result_value) is pbItem.pbQString:
            result_value = result_value.value
        if type(result_value) is unicode:
            result_value = str(result_value);
        if type(result_value) is objc.pyobjc_unicode:
            result_value = str(result_value);
        if type(result_value) is str:
            test_result_value = environment.parseKey(self.name, result_value, lookup_dict=lookup_dict);
            if test_result_value[0] == True:
                result_value = test_result_value[1];
            else:
                logging_helper.getLogger().error('[EnvVariable]: BAD VARIABLE :(');
        else:
            result_str = '';
            for item in result_value:
                result_str += str(item)+' ';
            result_value = result_str;
        if '$(inherited)' in result_value:
            inherited_value = self.inheritedValue();
            if inherited_value != None:
                inherited_value = inherited_value.value(environment, lookup_dict=lookup_dict);
            else:
                inherited_value = '';
            result_value = result_value.replace('$(inherited)', inherited_value);
        return result_value;
    
    @classmethod
    def commandLineArgsPropNames(cls):
        return ['CommandLinePrefixFlag', 'CommandLineArgs', 'CommandLineFlag'];
    
    def hasCommandLineArgs(self):
        return len(filter(lambda item: hasattr(self, item) and getattr(self, item) != None, EnvVariable.commandLineArgsPropNames())) > 0;
    
    def commandLineFlag(self, environment, lookup_dict=None):
        if lookup_dict == None:
            lookup_dict = environment.resolvedValues();
        
        flag_list = [];
        
        output = '';
        
        prefix_flag = '';
        if hasattr(self, 'CommandLinePrefixFlag') == True:
            prefix_flag = self.CommandLinePrefixFlag;
        
        primary_flag = '';
        flag_lookup_keys = [];
        flag_lookup_values = {};
        if hasattr(self, 'CommandLineArgs') == True:
            if hasattr(self.CommandLineArgs, 'keys') and callable(getattr(self.CommandLineArgs, 'keys')):
                for key in self.CommandLineArgs.keys():
                    flag_lookup_values[str(key)] = self.CommandLineArgs[key];
                flag_lookup_keys = list(map(lambda item: str(item), self.CommandLineArgs.keys()));
            elif len(self.CommandLineArgs) > 0:
                args_list = map(lambda item: str(item), self.CommandLineArgs);
                if hasattr(self, 'AllowedValues') == True:
                    flag_lookup_keys = list(map(lambda item: str(item), getattr(self, 'AllowedValues')));
                    for key in flag_lookup_keys:
                        flag_lookup_values[str(key)] = args_list
                else:
                    primary_flag = ' '.join(args_list);
        
        if hasattr(self, 'CommandLineFlag') == True:
            primary_flag = self.CommandLineFlag;
        
        value = self.value(environment, lookup_dict=lookup_dict);
        
        if hasattr(self, 'CommandLinePrefixFlag') == True or hasattr(self, 'CommandLineArgs') == True:
            if self.isList():
                value_list = filter(lambda item: len(item) > 0, value.split(' '));
                if len(flag_lookup_keys) > 0:
                    if value in flag_lookup_values.keys():
                        flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                    elif '<<otherwise>>' in flag_lookup_keys:
                        flag_list = map(lambda item: str(item), flag_lookup_values['<<otherwise>>']);
                    else:
                        logging_helper.getLogger().warn('[EnvVariable]: Error in parsing flag_lookup_values: %s' % flag_lookup_values);
                else:
                    # use primary flag
                    for item in value_list:
                        flag_list.append(primary_flag.replace('$(value)', item));
            elif self.isString() or self.isPath():
                value = str(value);
                if len(flag_lookup_values) > 0:
                    if value in flag_lookup_values.keys():
                        flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                    elif '<<otherwise>>' in flag_lookup_keys:
                        flag_list = map(lambda item: str(item), flag_lookup_values['<<otherwise>>']);
                    else:
                        logging_helper.getLogger().warn('[EnvVariable]: Error in parsing flag_lookup_values: %s' % flag_lookup_values);
                else:
                    # prefix flag check
                    flag_list.append(str(prefix_flag).replace('$(value)', value)+value);
            elif self.isBoolean():
                value = str(value);
                if value in flag_lookup_keys:
                    flag_list = map(lambda item: str(item), flag_lookup_values[value]);
            elif self.isEnum():
                value = str(value);
                if hasattr(self, 'AllowedValues') == True:
                    value_list = list(map(lambda item: str(item), getattr(self, 'AllowedValues')));
                    if value in value_list and value in flag_lookup_values.keys():
                        flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                    elif value in flag_lookup_values.keys():
                        flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                    elif '<<otherwise>>' in flag_lookup_keys:
                        flag_list = map(lambda item: str(item), flag_lookup_values['<<otherwise>>']);
                    else:
                        logging_helper.getLogger().error('[EnvVariable]: Value "%s" not allowed (%s) for %s' % (value, str(value_list), self.name));
                elif hasattr(self, 'Values') == True:
                    value_list = list(map(lambda item: str(item), getattr(self, 'Values')));
                    if value in value_list and value in flag_lookup_values.keys():
                        flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                    elif value in flag_lookup_values.keys():
                        flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                    elif '<<otherwise>>' in flag_lookup_keys:
                        flag_list = map(lambda item: str(item), flag_lookup_values['<<otherwise>>']);
                    else:
                        logging_helper.getLogger().warn('[EnvVariable]: Value "%s" not found in (%s) for %s, going to use anyway' % (value, str(value_list), self.name));
                else:
                    logging_helper.getLogger().warn('[EnvVariable]: Could not find Enumation Values on %s, going to use "%s" anyway' % (self.name, value));
            else:
                logging_helper.getLogger().error('[EnvVariable]: Unknown variable type!');
        elif hasattr(self, 'CommandLineFlag') == True:
            if self.isList():
                value_list = filter(lambda item: len(item) > 0, value.split(' '));
            elif self.isString() or self.isPath():
                value = str(value);
                if value != '':
                    flag_list.append(primary_flag);
                    flag_list.append(value);
            elif self.isBoolean():
                value = str(value);
                if value == 'YES' or value == 'True':
                    flag_list.append(primary_flag);
            elif self.isEnum():
                value = str(value);
            else:
                logging_helper.getLogger().error('[EnvVariable]: Unknown variable type!');
        
        output = ' '.join(map(lambda item: str(item).replace('$(value)', value), flag_list));
        output = environment.parseKey(self.name, output, lookup_dict=lookup_dict)[1];
        return output;