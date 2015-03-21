from .PBXResolver import *
from .PBX_Base_Target import *
from .PBX_Constants import *

class PBXLegacyTarget(PBX_Base_Target):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXLegacyTarget, self).__init__(lookup_func, dictionary, project, identifier);
        if kPBX_TARGET_buildSettings in dictionary.keys():
            self.buildSettings = dictionary[kPBX_TARGET_buildSettings];
        if kPBX_TARGET_passBuildSettingsInEnvironment in dictionary.keys():
            self.passBuildSettingsInEnvironment = dictionary[kPBX_TARGET_passBuildSettingsInEnvironment];
        if kPBX_TARGET_buildArgumentsString in dictionary.keys():
            self.buildArgumentsString = dictionary[kPBX_TARGET_buildArgumentsString];
        if kPBX_TARGET_buildToolPath in dictionary.keys():
            self.buildToolPath = dictionary[kPBX_TARGET_buildToolPath];
        if kPBX_TARGET_buildWorkingDirectory in dictionary.keys():
            self.buildWorkingDirectory = dictionary[kPBX_TARGET_buildWorkingDirectory];
        if kPBX_TARGET_settingsToExpand in dictionary.keys():
            self.settingsToExpand = dictionary[kPBX_TARGET_settingsToExpand];
        if kPBX_TARGET_settingsToPassInEnvironment in dictionary.keys():
            self.settingsToPassInEnvironment = dictionary[kPBX_TARGET_settingsToPassInEnvironment];
        if kPBX_TARGET_settingsToPassOnCommandLine in dictionary.keys():
            self.settingsToPassOnCommandLine = dictionary[kPBX_TARGET_settingsToPassOnCommandLine];
        if kPBX_TARGET_shouldUseHeadermap in dictionary.keys():
            self.shouldUseHeadermap = dictionary[kPBX_TARGET_shouldUseHeadermap];