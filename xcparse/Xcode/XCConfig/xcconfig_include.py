from .xcconfig_item_base import *

class xcconfig_include(xcconfig_item_base):
    
    def __init__(self, line):
        super(xcconfig_include, self).__init__(line);
        self.type = 'INCLUDE';