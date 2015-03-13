import os
from ..plist_helper import *

class xcsdk(object):
    
    def __init__(self, path):
        self.path = path;
        self.name = os.path.basename(path);
        
        settings_path = os.path.join(path, 'SDKSettings.plist');
        self.settings = LoadPlistFromDataAtPath(settings_path);