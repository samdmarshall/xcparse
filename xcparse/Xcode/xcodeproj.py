from __future__ import absolute_import
from .xc_base import xc_base
from ..Helpers import plist_helper
from ..Helpers import path_helper
from .PBX import PBXResolver

class xcodeproj(xc_base):
    
    def __init__(self, xcproj_path):
        """
        Pass the path to the '.xcodeproj' file to initialize the xcodeproj object.
        """
        self.contents = None;
        self.identifier = '';
        self.path = '';
        if xcproj_path.endswith('.xcodeproj') or xcproj_path.endswith('.pbproj'):
            self.path = path_helper(xcproj_path, 'project.pbxproj');
            
            self.contents = plist_helper.LoadPlistFromDataAtPath(self.path.root_path);
            if self.contents != None:
                self.identifier = self.contents['rootObject'];
                result = PBXResolver(self.objects()[self.identifier])
                if result[0] == True:
                    self.rootObject = result[1](PBXResolver, self.objects()[self.identifier], self, self.identifier);
                else:
                    self.rootObject = None;
            else:
                print 'Could not load contents of plist!';
        else:
            print 'Not a xcode project file!';
    
    def __repr__(self):
        if self.isValid():
            return '(%s : %s : %s)' % (type(self), self.path, self.identifier);
        else:
            return '(%s : INVALID OBJECT)' % (type(self));
    
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
        objects = {};
        if self.isValid():
            objects = self.contents['objects'];
        return objects;
    
    def projects(self):
        """
        This method returns a list of 'xcodeproj' objects that represents any referenced 
        xcodeproj files in this project.
        """
        subprojects = [];
        if self.isValid():
            for path in self.__subproject_paths():
                project = xcodeproj(path);
                subprojects.append(project);
                subprojects.extend(project.projects());
        return set(subprojects);
        
    
    def __subproject_paths(self):
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
                    subproject_path = os.path.join(self.path.base_path, file_ref.path.obj_path);
                    if os.path.exists(subproject_path) == True:
                        paths.append(subproject_path);
        return paths;
    
    def targets(self):
        """
        This method will return a list of build targets that are associated with this xcodeproj.
        """
        targets = [];
        if self.isValid():
            targets.extend(self.rootObject.targets);
        return targets;
    