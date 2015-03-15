import re
from .xcconfig_item_base import *

class xcconfig_kv(xcconfig_item_base):
    
    def __init__(self, line):
        super(xcconfig_kv, self).__init__(line);
        self.type = 'KV';
        offset = xcconfig_kv.FindKeyValueAssignmentOffset(self.contents, 0);
        self.__key = self.contents[:offset];
        self.__value = self.contents[offset+1:];
    
    @classmethod
    def FindKeyValueAssignmentOffset(cls, line, offset):
        find_open_bracket = line.find('[');
        find_equals = line.find('=');
        new_offset = offset;
        if find_open_bracket != -1:
            # conditional bracket
            find_close_bracket = line.find(']');
            if find_close_bracket != -1:
                find_close_bracket += 1;
                # found conditional bracket close
                new_offset += find_close_bracket;
                return xcconfig_kv.FindKeyValueAssignmentOffset(line[find_close_bracket:], new_offset);
            else:
                print 'error!';
                return -1;
        else:
            if find_equals != -1:
                new_offset += find_equals;
            return new_offset;
    
    def key(self):
        key = self.__key;
        find_bracket = key.find('[');
        if find_bracket == -1:
            return key;
        else:
            return key[:find_bracket];
    
    def conditions(self):
        conditions = {};
        key = self.__key;
        find_bracket = key.find('[');
        if find_bracket != -1:
            key_conditions_string = key[find_bracket:];
            condition_strings = filter(lambda cond_string: cond_string != '' and cond_string != ' ', re.split(r'[\[|\]]', key_conditions_string));
            for condition in condition_strings:
                equals_offset = condition.find('=');
                cond_key = condition[:equals_offset];
                cond_value = condition[equals_offset+1:];
                conditions[cond_key] = cond_value;
        return conditions;
    
    def value(self, value_type):
        value = self.__value;
        if value[0] == ' ':
            value = value[1:];
        if value_type == None:
            return value;
        else:
            if value_type == 'string':
                return str(value);
            if value_type == 'stringlist':
                # this has to change to be separated by strings
                return list(value);