from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *

class PBXShellScriptBuildPhase(object):
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
            fileList = [];
            for file in dictionary['files']:
                result = lookup_func(project.objects()[file]);
                if result[0] == True:
                    fileList.append(result[1](lookup_func, project.objects()[file], project));
            self.files = fileList;
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
    
    def performPhase(self):
        print 'implement me!';