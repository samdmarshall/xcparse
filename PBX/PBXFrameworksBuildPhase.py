from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXFrameworksBuildPhase(PBX_Base_Phase):
    # buildActionMask = '';
    # files = [];
    # runOnlyForDeploymentPostprocessing = 0;
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        self.phase_type = 'Link Libraries';
        if 'buildActionMask' in dictionary.keys():
            self.buildActionMask = dictionary['buildActionMask'];
        if 'files' in dictionary.keys():
            self.files = self.parseProperty('files', lookup_func, dictionary, project, True);
        if 'runOnlyForDeploymentPostprocessing' in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary['runOnlyForDeploymentPostprocessing'];
    