from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *

class PBXFrameworkBuildPhase(object):
    # buildActionMask = '';
    # files = [];
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
    
    def performPhase(self):
        print 'implement me!';