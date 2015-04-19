import os
from ...Helpers import logging_helper
from ...Helpers import xcrun_helper

class xccompiler(object):
    
    def __init__(self, compiler, config_dict):
        self.compiler = compiler;
        self.properties = config_dict;
    
    # add something to allow for additional flags to be passed
    
    def build(self):
        if isinstance(self, xccompiler) == True:
            logging_helper.getLogger().error('[xccompiler]: base xccompiler object doesn\'t have compiler specific logic');