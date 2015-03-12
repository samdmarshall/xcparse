from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXSourcesBuildPhase(PBX_Base_Phase):
    # buildActionMask = 0;
    # files = [];
    # runOnlyForDeploymentPostprocessing = 0;
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.bundleid = 'com.apple.buildphase.sources';
        self.identifier = identifier;
        self.phase_type = 'Compile Sources';
        self.files = [];
        if 'buildActionMask' in dictionary.keys():
            self.buildActionMask = dictionary['buildActionMask'];
        if 'files' in dictionary.keys():
            self.files = self.parseProperty('files', lookup_func, dictionary, project, True);
        if 'runOnlyForDeploymentPostprocessing' in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary['runOnlyForDeploymentPostprocessing'];
    
    def performPhase(self, build_system, target):
        phase_spec = build_system.getSpecForIdentifier(self.bundleid);
        print '%s Phase: %s' % (self.phase_type, phase_spec.name);
        print '* %s' % (phase_spec.contents['Description']);
        
        compiler_specs = build_system.getSpecForType('Compiler');
        
        for file in self.files:
            file_spec = build_system.getSpecForIdentifier(file.fileRef.ftype);
            compiler = build_system.getCompilerForFileReference(file.fileRef);
        
        print '(implement me!)';
        print '';