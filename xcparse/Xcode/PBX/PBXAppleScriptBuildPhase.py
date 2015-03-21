from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXAppleScriptBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXAppleScriptBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.applescript';
        self.phase_type = 'AppleScript';
        if 'buildActionMask' in dictionary.keys():
            self.buildActionMask = dictionary['buildActionMask'];
        if 'contextName' in dictionary.keys():
            self.buildActionMask = dictionary['contextName'];
        if 'files' in dictionary.keys():
            self.files = self.parseProperty('files', lookup_func, dictionary, project, True);
        if 'runOnlyForDeploymentPostprocessing' in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary['runOnlyForDeploymentPostprocessing'];
        if 'isSharedContext' in dictionary.keys():
            self.isSharedContext = dictionary['isSharedContext'];