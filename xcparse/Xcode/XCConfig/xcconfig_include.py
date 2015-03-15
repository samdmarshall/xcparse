import os
from .xcconfig_item_base import *
from ...Helpers import xcrun_helper

class xcconfig_include(xcconfig_item_base):
    
    def __init__(self, line):
        super(xcconfig_include, self).__init__(line);
        self.type = 'INCLUDE';
    
    def includePath(self, base_path):
        quote_start = self.contents.find('"');
        path = self.contents[quote_start:];
        quote_end = path.find('"');
        path = path[:quote_end];
        if path.startswith('<DEVELOPER_DIR>'):
            path = path.replace('<DEVELOPER_DIR>', xcrun_helper.resolve_developer_path(), 1);
        if path[0] != '/':
            path = os.path.join(base_path, path);
        return os.path.normpath(path);