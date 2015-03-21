from .PBXResolver import *
from .PBX_Base_Phase import *
from .PBX_Constants import *

class PBXCopyFilesBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXCopyFilesBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.copy-files';
        self.phase_type = 'Copy Files';
        if kPBX_PHASE_dstPath in dictionary.keys():
            self.dstPath = dictionary[kPBX_PHASE_dstPath];
        if kPBX_PHASE_dstSubfolderSpec in dictionary.keys():
            self.dstSubfolderSpec = dictionary[kPBX_PHASE_dstSubfolderSpec];
        