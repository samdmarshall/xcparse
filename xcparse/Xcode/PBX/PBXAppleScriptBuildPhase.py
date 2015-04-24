from .PBXResolver import *
from .PBX_Base_Phase import *
from .PBX_Constants import *

class PBXAppleScriptBuildPhase(PBX_Base_Phase):
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXAppleScriptBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.applescript';
        self.phase_type = 'AppleScript';
        if kPBX_PHASE_contextName in dictionary.keys():
            self.contextName = dictionary[kPBX_PHASE_contextName];
        if kPBX_PHASE_isSharedContext in dictionary.keys():
            self.isSharedContext = dictionary[kPBX_PHASE_isSharedContext];