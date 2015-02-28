from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base import *

class PBXProject(PBX_Base):
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
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'attributes' in dictionary.keys():
            self.attributes = dictionary['attributes'];
        if 'buildConfigurationList' in dictionary.keys():
            self.buildConfigurationList = self.parseProperty('buildConfigurationList', lookup_func, dictionary, project, False);
        if 'compatibilityVersion' in dictionary.keys():
            self.compatibilityVersion = dictionary['compatibilityVersion'];
        if 'developmentRegion' in dictionary.keys():
            self.developmentRegion = dictionary['developmentRegion'];
        if 'hasScannedForEncodings' in dictionary.keys():
            self.hasScannedForEncodings = dictionary['hasScannedForEncodings'];
        if 'knownRegions' in dictionary.keys():
            self.knownRegions = dictionary['knownRegions'];
        if 'mainGroup' in dictionary.keys():
            self.mainGroup = self.parseProperty('mainGroup', lookup_func, dictionary, project, False);
        if 'productRefGroup' in dictionary.keys():
            self.productRefGroup = dictionary['productRefGroup'];
        if 'projectDirPath' in dictionary.keys():
            self.projectDirPath = dictionary['projectDirPath'];
        if 'projectReferences' in dictionary.keys():
            self.projectReferences = dictionary['projectReferences'];
        if 'projectRoot' in dictionary.keys():
            self.projectRoot = dictionary['projectRoot'];
        if 'targets' in dictionary.keys():
            self.targets = self.parseProperty('targets', lookup_func, dictionary, project, True);