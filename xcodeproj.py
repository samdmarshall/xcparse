from __future__ import absolute_import
import Cocoa
import Foundation
import os
import sys

from .Path import *

from .xcscheme import *

from .PBX.PBXResolver import PBXResolver

class xcodeproj(object):
    # path = {};
    # contents = {};
    # rootObject = {};
    
    def __init__(self, xcproj_path):
        if xcproj_path.endswith('.xcodeproj') or xcproj_path.endswith('.pbproj'):
            self.path = Path(xcproj_path, 'project.pbxproj');
            
            if os.path.exists(self.path.root_path) == True:
                # loading project file
                plistNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(self.path.root_path, Foundation.NSUncachedRead, None);
                if errorMessage == None:
                    plistContents, plistFormat, errorMessage = Foundation.NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(plistNSData, Foundation.NSPropertyListMutableContainers, None, None);
                    if errorMessage == None:
                        self.contents = plistContents;
                        self.identifier  = self.contents['rootObject'];
                        result = PBXResolver(self.objects()[self.identifier])
                        if result[0] == True:
                            self.rootObject = result[1](PBXResolver, self.objects()[self.identifier], self, self.identifier);
                        else:
                            self.rootObject = {};
                    else:
                        print errorMessage;
                else:
                    print errorMessage;
            else:
                print 'Invalid xcodeproj file!';
    
    def __attrs(self):
        return (self.identifier, self.path);

    def __eq__(self, other):
        return isinstance(other, xcodeproj) and self.identifier == other.identifier and self.path.root_path == other.path.root_path;

    def __hash__(self):
        return hash(self.__attrs());
    
    def isValid(self):
        return self.contents != {};
    
    def objects(self):
        return self.contents['objects'];
    
    def projects(self):
        subprojects = [];
        for path in self.subproject_paths():
            project = xcodeproj(path);
            subprojects.append(project);
            subprojects.extend(project.projects());
        return set(subprojects);
    
    def subproject_paths(self):
        paths = [];
        root_obj = self.objects()[self.identifier];
        if 'projectReferences' in root_obj.keys():
            for project_dict in root_obj['projectReferences']:
                project_ref = project_dict['ProjectRef'];
                result = PBXResolver(self.objects()[project_ref]);
                if result[0] == True:
                    file_ref = result[1](PBXResolver, self.objects()[project_ref], self);
                    subproject_path = os.path.join(self.path.base_path, file_ref.path);
                    if os.path.exists(subproject_path) == True:
                        paths.append(subproject_path);
        return paths;
    
    def targets(self):
        if self.rootObject != {}:
            return self.rootObject.targets;
        else:
            return [];
    
    def schemes(self):
        schemes = [];
        # shared schemes
        shared_path = XCSchemeGetSharedPath(self.path.obj_path);
        shared_schemes = XCSchemeParseDirectory(shared_path);
        for scheme in shared_schemes:
            scheme.shared = True;
        # user schemes
        user_path = XCSchemeGetUserPath(self.path.obj_path);
        user_schemes = XCSchemeParseDirectory(user_path);
        # merge schemes
        for scheme in shared_schemes + user_schemes:
            scheme.container = self.path;
            schemes.append(scheme);
        return schemes;
    
    def hasSchemeWithName(self, scheme_name):
        schemes = self.schemes();
        result = scheme_name in list(map(XCSchemeName, schemes));
        found_scheme = {};
        for scheme in schemes:
            if scheme.name == scheme_name:
                found_scheme = scheme;
                break;
        return (result, found_scheme);
    