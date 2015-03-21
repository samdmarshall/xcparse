from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXHeadersBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXHeadersBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.headers';
        self.phase_type = 'Copy Headers';
        if 'buildActionMask' in dictionary.keys():
            self.buildActionMask = dictionary['buildActionMask'];
        if 'files' in dictionary.keys():
            self.files = self.parseProperty('files', lookup_func, dictionary, project, True);
        if 'runOnlyForDeploymentPostprocessing' in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary['runOnlyForDeploymentPostprocessing'];