from __future__ import absolute_import
import os
import importlib

from .xcodeproj import *
from .xcworkspace import *
from .xcscheme import *

class xcparse(object):
    # root = {};
    # projects = [];
    # name = '';
    # root_path = '';
    
    def __init__(self, path):
        if os.path.exists(path) == True:
            self.root_path = os.path.abspath(path);
            self.name = os.path.basename(path);
            if self.name.endswith('.xcodeproj') or self.name.endswith('.pbproj'):
                project_file = xcodeproj(self.root_path);
                self._projects = [];
                for project in project_file.projects():
                    self._projects.append(project);
                self.root = project_file;
            elif self.name.endswith('.xcworkspace'):
                workspace_file = xcworkspace(self.root_path);
                self.root = workspace_file;
                self._projects = [];
                for project_file in workspace_file.projects():
                    self._projects.append(project_file);
            else:
                print 'Invalid file!';
        else:
            print 'Could not find file!';
    
    def projects(self):
        project_list = [self.root];
        project_list.extend(self._projects);
        return project_list;
    
    def schemes(self):
        project_schemes = [];
        for project_file in self.projects():
            for scheme in project_file.schemes():
                project_schemes.append(scheme);
        return project_schemes;
    
    def schemeNameSet(self):
        return set(list(map(XCSchemeName, self.schemes())));
    
    def containerForSchemeWithName(self, scheme_name):
        scheme = {};
        container = {};
        found = False;
        for project in self.projects():
            result = project.hasSchemeWithName(scheme_name);
            found = result[0];
            if found == True:
                scheme = result[1];
                container = project;
                break;
        return (found, scheme, container);