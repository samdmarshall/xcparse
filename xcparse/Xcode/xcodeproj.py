from __future__ import absolute_import
from .xc_base import xc_base
from .PBX import PBXResolver
from .PBX.PBX_Constants import *
from ..Helpers import plist_helper
from ..Helpers import path_helper
from ..Helpers import logging_helper

class xcodeproj(xc_base):
    
    def __init__(self, xcproj_path):
        """
        Pass the path to the '.xcodeproj' file to initialize the xcodeproj object.
        """
        self.contents = None;
        self.identifier = '';
        self.path = '';
        self.rootObject = None;
        self.objects = set();
        if xcproj_path.endswith('.xcodeproj') or xcproj_path.endswith('.pbproj'):
            self.path = path_helper(xcproj_path, 'project.pbxproj');
            
            self.contents = plist_helper.LoadPlistFromDataAtPath(self.path.root_path);
            if self.contents != None:
                for item in self.contents[kPBX_objects]:
                    find_object = self.objectForIdentifier(item);
                    if find_object == None:
                        result = PBXResolver(self.contents[kPBX_objects][item])
                        if result[0] == True:
                            resolved_object = result[1](PBXResolver, self.contents[kPBX_objects][item], self, item);
                            self.objects.add(resolved_object);
                    else:
                        self.objects.add(find_object);
                self.identifier = self.contents['rootObject'];
                self.rootObject = self.objectForIdentifier(self.identifier);
                # result = PBXResolver(self.contents['objects'][self.identifier])
                # if result[0] == True:
                #     self.rootObject = result[1](PBXResolver, self.contents['objects'][self.identifier], self, self.identifier);
                # else:
                #     logging_helper.getLogger().error('[xcodeproj]: Error in parsing project file!');
            else:
                logging_helper.getLogger().error('[xcodeproj]: Could not load contents of plist!');
        else:
            logging_helper.getLogger().error('[xcodeproj]: Not a xcode project file!');
    
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
    
    def objectForIdentifier(self, identifier):
        result = None;
        if self.isValid():
            filter_results = filter(lambda obj: obj.identifier == identifier, self.objects);
            if len(filter_results) > 0:
                result = filter_results[0];
        return result;
    
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
                file_ref = None;
                project_ref = project_dict['ProjectRef'];
                found_object = self.objectForIdentifier(project_ref);
                if found_object != None:
                    file_ref = found_object;
                else:
                    result = PBXResolver(self.contents[kPBX_objects][project_ref]);
                    if result[0] == True:
                        file_ref = result[1](PBXResolver, self.contents[kPBX_objects][project_ref], self, project_ref);
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
    