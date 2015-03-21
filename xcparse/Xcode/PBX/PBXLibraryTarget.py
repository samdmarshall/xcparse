from .PBXResolver import *
from .PBX_Base_Target import *
from .PBX_Constants import *

class PBXLibraryTarget(PBX_Base_Target):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXLibraryTarget, self).__init__(lookup_func, dictionary, project, identifier);
        if kPBX_TARGET_passBuildSettingsInEnvironment in dictionary.keys():
            self.passBuildSettingsInEnvironment = dictionary[kPBX_TARGET_passBuildSettingsInEnvironment];
        if kPBX_TARGET_buildArgumentsString in dictionary.keys():
            self.buildArgumentsString = dictionary[kPBX_TARGET_buildArgumentsString];
        if kPBX_TARGET_buildToolPath in dictionary.keys():
            self.buildToolPath = dictionary[kPBX_TARGET_buildToolPath];