from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXJavaArchiveBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXJavaArchiveBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.java-archive'
        self.phase_type = 'Java Archive';
    