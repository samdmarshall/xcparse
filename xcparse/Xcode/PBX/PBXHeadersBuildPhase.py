from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXHeadersBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXHeadersBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.headers';
        self.phase_type = 'Copy Headers';
        