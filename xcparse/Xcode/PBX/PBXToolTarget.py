from .PBXResolver import *
from .PBX_Base_Target import *
from .PBX_Constants import *

class PBXToolTarget(PBX_Base_Target):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXToolTarget, self).__init__(lookup_func, dictionary, project, identifier);
        if kPBX_TARGET_buildSettings in dictionary.keys():
            self.buildSettings = dictionary[kPBX_TARGET_buildSettings];
        if kPBX_TARGET_productInstallPath in dictionary.keys():
            self.productInstallPath = dictionary[kPBX_TARGET_productInstallPath];
        if kPBX_TARGET_productSettingsXML in dictionary.keys():
            self.productSettingsXML = dictionary[kPBX_TARGET_productSettingsXML];
        if kPBX_TARGET_shouldUseHeadermap in dictionary.keys():
            self.shouldUseHeadermap = dictionary[kPBX_TARGET_shouldUseHeadermap];