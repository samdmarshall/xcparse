import os
import sys
import Path


class xcconfig(object):
    
    def __init__(self, path):
        self.path = path;
        
    def valueForKey(self, key):
        return None;