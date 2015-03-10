from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXRezBuildPhase(PBX_Base_Phase):
    # buildActionMask = 0;
    # files = [];
    # runOnlyForDeploymentPostprocessing = 0;
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.bundleid = 'com.apple.buildphase.rez';
        self.identifier = identifier;
        if 'buildActionMask' in dictionary.keys():
            self.buildActionMask = dictionary['buildActionMask'];
        if 'files' in dictionary.keys():
            self.files = self.parseProperty('files', lookup_func, dictionary, project, True);
        if 'runOnlyForDeploymentPostprocessing' in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary['runOnlyForDeploymentPostprocessing'];
    