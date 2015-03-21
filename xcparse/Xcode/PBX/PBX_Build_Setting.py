from .PBXResolver import *
from .PBX_Base import *
from ..XCConfig import xcconfig

class PBX_Build_Setting(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBX_Build_Setting, self).__init__(lookup_func, dictionary, project, identifier);
    
    def loadBuildSettings(self):
        self.xcconfig = xcconfig(None);
    
    def buildSettings(self, configuration_name):
        """
        This method will return a dictionary of build settings for the level of the object
        """
        settings = {};
        #if hasattr(self, 'buildConfigurationList'):
            
        return settings;