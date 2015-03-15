from .xcconfig_item_base import *

class xcconfig_kv(xcconfig_item_base):
    
    def __init__(self, line):
        super(xcconfig_kv, self).__init__(line);
        self.type = 'KV';
        offset = xcconfig_kv.FindKeyValueAssignmentOffset(self.contents, 0);
        self.key = self.contents[:offset];
        self.value = self.contents[offset+1:];
        
    @classmethod
    def FindKeyValueAssignmentOffset(cls, line, offset):
        find_equals = line.find('=');
        find_open_bracket = line.find('[');
        if find_open_bracket == -1:
            return offset + find_equals;
        else:
            if find_open_bracket < find_equals:
                new_offset = offset + find_equals + 1;
                return xcconfig_kv.FindKeyValueAssignmentOffset(line[new_offset:], new_offset);
            else:
                return offset + find_equals;