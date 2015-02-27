from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *

class PBXProject(object):
    # attributes = {};
    # buildConfigurationList = {};
    # compatibilityVersion = '';
    # developmentRegion = '';
    # hasScannedForEncodings = 0;
    # knownRegions = [];
    # mainGroup = {};
    # projectDirPath = '';
    # projectRoot = '';
    # targets = [];
    
    def __init__(self, lookup_func, dictionary, project):
        if 'attributes' in dictionary.keys():
            self.attributes = dictionary['attributes'];
        if 'buildConfigurationList' in dictionary.keys():
            result = lookup_func(project.objects()[dictionary['buildConfigurationList']])
            if result[0] == True:
                self.buildConfigurationList = result[1](lookup_func, project.objects()[dictionary['buildConfigurationList']], project);
        if 'compatibilityVersion' in dictionary.keys():
            self.compatibilityVersion = dictionary['compatibilityVersion'];
        if 'developmentRegion' in dictionary.keys():
            self.developmentRegion = dictionary['developmentRegion'];
        if 'hasScannedForEncodings' in dictionary.keys():
            self.hasScannedForEncodings = dictionary['hasScannedForEncodings'];
        if 'knownRegions' in dictionary.keys():
            self.knownRegions = dictionary['knownRegions'];
        if 'mainGroup' in dictionary.keys():
            result = lookup_func(project.objects()[dictionary['mainGroup']])
            if result[0] == True:
                self.mainGroup = result[1](lookup_func, project.objects()[dictionary['mainGroup']], project);
        if 'projectDirPath' in dictionary.keys():
            self.projectDirPath = dictionary['projectDirPath'];
        if 'projectRoot' in dictionary.keys():
            self.projectRoot = dictionary['projectRoot'];
        if 'targets' in dictionary.keys():
            targetList = [];
            for target in dictionary['targets']:
                result = lookup_func(project.objects()[target]);
                if result[0] == True:
                    targetList.append(result[1](lookup_func, project.objects()[target], project));
            self.targets = targetList;