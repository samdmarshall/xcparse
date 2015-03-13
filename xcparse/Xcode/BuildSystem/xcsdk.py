import os
from ...Helpers import plist_helper

class xcsdk(object):
    
    def __init__(self, path):
        self.path = path;
        self.name = os.path.basename(path);
        
        settings_path = os.path.join(path, 'SDKSettings.plist');
        self.settings = plist_helper.LoadPlistFromDataAtPath(settings_path);