from ..xcconfig import *
from .PBXResolver import *

class PBX_Build_Setting(object):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.name = 'PBX_BUILD_SETTING';
        self.identifier = identifier;
    
    def loadBuildSettings(self):
        self.xcconfig = xcconfig(None);
    
    def buildSettings(self, configuration_name):
        """
        This method will return a dictionary of build settings for the level of the object
        """
        settings = {};
        #if hasattr(self, 'buildConfigurationList'):
            
        return settings;