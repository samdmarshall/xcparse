from .xcconfig_item_base import *

class xcconfig_comment(xcconfig_item_base):
    
    def __init__(self, line):
        super(xcconfig_comment, self).__init__(line);
        self.type = 'COMMENT';