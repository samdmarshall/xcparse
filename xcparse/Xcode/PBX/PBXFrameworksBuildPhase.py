from .PBX_Base_Phase import *

class PBXFrameworksBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXFrameworksBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.frameworks';
        self.phase_type = 'Link Libraries';
    