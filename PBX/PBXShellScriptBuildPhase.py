from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXShellScriptBuildPhase(PBX_Base_Phase):
    # buildActionMask = 0;
    # files = [];
    # inputPaths = [];
    # outputPaths = [];
    # shellPath = '';
    # shellScript = '';
    # runOnlyForDeploymentPostprocessing = 0;
    
    def __init__(self, lookup_func, dictionary, project):
        if 'buildActionMask' in dictionary.keys():
            self.buildActionMask = dictionary['buildActionMask'];
        if 'files' in dictionary.keys():
            self.files = self.parseProperty('files', lookup_func, dictionary, project, True);
        if 'runOnlyForDeploymentPostprocessing' in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary['runOnlyForDeploymentPostprocessing'];
        if 'shellScript' in dictionary.keys():
            self.shellScript = dictionary['shellScript'];
        if 'shellPath' in dictionary.keys():
            self.shellPath = dictionary['shellPath'];
        if 'inputPaths' in dictionary.keys():
            inputPaths = [];
            for inputPath in dictionary['inputPaths']:
                inputPaths.append(inputPath);
            self.inputPaths = inputPaths;
        if 'outputPaths' in dictionary.keys():
            outputPaths = [];
            for outputPath in dictionary['outputPaths']:
                outputPaths.append(outputPath);
            self.outputPaths = outputPaths;