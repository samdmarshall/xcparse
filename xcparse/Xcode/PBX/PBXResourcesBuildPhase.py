from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXResourcesBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXResourcesBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.resources';
        self.phase_type = 'Copy Resources';