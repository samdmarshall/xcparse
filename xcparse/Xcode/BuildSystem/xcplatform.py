import os

from ...Helpers import plist_helper
from ...Helpers import path_helper
from ...Helpers import xcrun_helper
from .xcsdk import *

def LoadPlatforms():
    platforms = list();
    platform_dir_path = os.path.join(xcrun_helper.resolve_developer_path(), 'Platforms');
    if os.path.exists(platform_dir_path) == True:
        for platform_bundle in os.listdir(platform_dir_path):
            platform_path = os.path.join(platform_dir_path, platform_bundle);
            platforms.append(xcplatform(platform_path));
    return platforms;

class xcplatform(object):
    
    def __init__(self, path):
        self.path = path;
        self.name = os.path.basename(path);
            
        info_path = os.path.join(path, 'Info.plist');
        self.info = plist_helper.LoadPlistFromDataAtPath(info_path);
    
        self.sdks = list();
        sdk_dir_path = os.path.join(self.path, 'Developer/SDKs');
        if os.path.exists(sdk_dir_path) == True:
            for sdk_bundle in os.listdir(sdk_dir_path):
                sdk_path = os.path.join(sdk_dir_path, sdk_bundle);
                self.sdks.append(xcsdk(sdk_path));
        