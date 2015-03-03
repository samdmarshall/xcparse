from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base import *
from .PBX_Build_Setting import *

class PBXProject(PBX_Base, PBX_Build_Setting):
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
        self.name = os.path.basename(project.path.obj_path);
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
        else:
            self.projectReferences = [];
        if 'projectRoot' in dictionary.keys():
            self.projectRoot = Path(project.path.base_path, dictionary['projectRoot']);
        if 'targets' in dictionary.keys():
            self.targets = self.parseProperty('targets', lookup_func, dictionary, project, True);
        else:
            self.targets = [];
        # populate with paths
        self.refreshItemPaths();
        self.loadBuildSettings();
    
    def refreshItemPaths(self):
        """
        This method will walk the project file and resolve the paths of items included in this project.
        """
        if isinstance(self.mainGroup, PBXGroup):
            self.mainGroup.resolvePath(self, self.projectRoot);
    
    def targetForProductRef(self, reference):
        """
        This method will return a list of targets that match a built product reference
        """
        return list(filter(lambda target: target.productReference.identifier == reference, self.targets));
    