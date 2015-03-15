from .xcconfig_item_base import xcconfig_item_base
from .xcconfig_include import xcconfig_include
from .xcconfig_comment import xcconfig_comment
from .xcconfig_kv import xcconfig_kv

def xcconfig_line_type(line):
    type = 'EMPTY';
    if line != None:
        if line.startswith('//') == True:
            type = 'COMMENT';
        elif line.startswith('#include ') == True:
            type = 'INCLUDE';
        else:
            offset = xcconfig_kv.FindKeyValueAssignmentOffset(line, 0);
            if offset > 0 and offset < len(line):
                type = 'KV';
    return type;

XCCONGIF_LINE_TYPE_DICT = {
    'COMMENT': xcconfig_comment,
    'INCLUDE': xcconfig_include,
    'KV': xcconfig_kv,
};

def xcconfig_line_resolver(line, type):
    global XCCONGIF_LINE_TYPE_DICT;
    if type in XCCONGIF_LINE_TYPE_DICT.keys():
        return (True, XCCONGIF_LINE_TYPE_DICT[type]);
    else:
        return (False, None);