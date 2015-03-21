from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXCopyFilesBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXCopyFilesBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.copy-files';
        self.phase_type = 'Copy Files';
        if 'buildActionMask' in dictionary.keys():
            self.buildActionMask = dictionary['buildActionMask'];
        if 'files' in dictionary.keys():
            self.files = self.parseProperty('files', lookup_func, dictionary, project, True);
        if 'runOnlyForDeploymentPostprocessing' in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary['runOnlyForDeploymentPostprocessing'];
        if 'dstPath' in dictionary.keys():
            self.dstPath = dictionary['dstPath'];
        if 'dstSubfolderSpec' in dictionary.keys():
            self.dstSubfolderSpec = dictionary['dstSubfolderSpec'];
        