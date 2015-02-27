from __future__ import absolute_import
import os
import importlib

from ..Logger import *

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
                self.projects = [];
                for project in project_file.projects():
                    self.projects.append(project);
                self.root = project_file;
            elif self.name.endswith('.xcworkspace'):
                workspace_file = xcworkspace(self.root_path);
                self.root = workspace_file;
                projects = [];
                for project_file in workspace_file.projects():
                    projects.append(project_file);
                self.projects = projects;
            else:
                Logger.debuglog([
                                Logger.colour('red',True),
                                Logger.string('%s', 'Invalid file!'),
                                Logger.colour('reset', True)
                                ]);
        else:
            Logger.debuglog([
                            Logger.colour('red',True),
                            Logger.string('%s', 'Could not find file!'),
                            Logger.colour('reset', True)
                            ]);
    
    def schemes(self):
        project_schemes = [];
        for project_file in self.projects:
            for scheme in project_file.schemes():
                project_schemes.append(scheme);
        root_schemes = self.root.schemes();
        return root_schemes + project_schemes;
    
    def schemeNameSet(self):
        return set(list(map(XCSchemeName, self.schemes())));
    
    def containerForSchemeWithName(self, scheme_name):
        scheme = {};
        container = {};
        found = False;
        searchableItems = self.projects;
        searchableItems.append(self.root);
        for project in searchableItems:
            result = project.hasSchemeWithName(scheme_name);
            found = result[0];
            if found == True:
                scheme = result[1];
                container = project;
                break;
        return (found, scheme, container);