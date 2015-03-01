from __future__ import absolute_import
import Cocoa
import Foundation

from .PBX.PBXResolver import PBXResolver

from .xc_base import *

class xcodeproj(xc_base):
    # path = {};
    # contents = {};
    # rootObject = {};
    
    def __init__(self, xcproj_path):
        self.contents = None;
        self.identifier = '';
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
                            self.rootObject = None;
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
        return self.contents != None;
    
    def objects(self):
        """
        This method returns a dictionary of raw objects from the parsed xcodeproject 
        file. The objects in this list are bridged from Cocoa.
        """
        if self.isValid():
            return self.contents['objects'];
        else:
            return {};
    
    def projects(self):
        """
        THis method returns a list of 'xcodeproj' objects that represents any referenced 
        xcodeproj files in this project.
        """
        subprojects = [];
        if self.isValid():
            for path in self.subproject_paths():
                project = xcodeproj(path);
                subprojects.append(project);
                subprojects.extend(project.projects());
        return set(subprojects);
        
    
    def subproject_paths(self):
        """
        This method is for returning a list of paths to referenced project files in this
        xcodeproj file.
        """
        paths = [];
        if self.isValid():
            for project_dict in self.rootObject.projectReferences:
                project_ref = project_dict['ProjectRef'];
                result = PBXResolver(self.objects()[project_ref]);
                if result[0] == True:
                    file_ref = result[1](PBXResolver, self.objects()[project_ref], self, project_ref);
                    subproject_path = os.path.join(self.path.base_path, file_ref.path);
                    if os.path.exists(subproject_path) == True:
                        paths.append(subproject_path);
        return paths;
    
    def targets(self):
        """
        This method will return a list of build targets that are associated with this xcodeproj.
        """
        if self.isValid():
            return self.rootObject.targets;
        else:
            return [];
    