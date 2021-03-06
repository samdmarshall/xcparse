from .PBX_Base import *
from ..XCConfig import xcconfig

class XCBuildConfiguration(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(XCBuildConfiguration, self).__init__(lookup_func, dictionary, project, identifier);
        if 'baseConfigurationReference' in dictionary.keys():
            self.baseConfigurationReference = self.parseProperty('baseConfigurationReference', lookup_func, dictionary, project, False);
        else:
            self.baseConfigurationReference = None;
        if 'buildSettings' in dictionary.keys():
            self.buildSettings = dictionary['buildSettings'];
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        
        # parse the xcconfig file
        if self.baseConfigurationReference != None:
            self.xcconfig = xcconfig(self.baseConfigurationReference.fs_path);
        else:
            # this needs to find the base config on the target
            self.xcconfig = None;
    
    def buildSettingForKey(self, key):
        return '';