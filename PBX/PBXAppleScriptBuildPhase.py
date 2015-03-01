from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXAppleScriptBuildPhase(PBX_Base_Phase):
    # buildActionMask = 0;
    # files = [];
    # isSharedContext = 0;
    # runOnlyForDeploymentPostprocessing = 0;
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        self.phase_type = 'AppleScript';
        if 'buildActionMask' in dictionary.keys():
            self.buildActionMask = dictionary['buildActionMask'];
        if 'files' in dictionary.keys():
            self.files = self.parseProperty('files', lookup_func, dictionary, project, True);
        if 'runOnlyForDeploymentPostprocessing' in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary['runOnlyForDeploymentPostprocessing'];
        if 'isSharedContext' in dictionary.keys():
            self.isSharedContext = dictionary['isSharedContext'];