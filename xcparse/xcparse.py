import os
import Xcode
from Xcode import xcodeproj
from .Helpers import logging_helper

class xcparse(object):
    def __init__(self, path):
        """
        Returns a xcparse object initialized from an xcodeproj or xcworkspace file.
        
        path should be the full path to a '.xcodeproj' or '.xcworkspace'.
        """
        self.project_constructor = xcodeproj; # this exists only to prevent recursive imports later
        self.path = '';
        self.root = None;
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
                logging_helper.getLogger().error('[xcparse]: Invalid file!');
        else:
            logging_helper.getLogger().error('[xcparse]: Could not find file!');
    
    def isValid(self):
        return self.name != '' and self.root != None;
    
    def projects(self):
        """
        This method returns a list of 'xcodeproj' objects, one for each of the referenced
        project files in whatever root project or workspace was loaded. If there are 
        multiple references to the same project file, this method will only one instance of that
        referenced project.
        """
        project_list = [];
        if self.isValid():
            project_list.append(self.root);
            project_list.extend(self._projects);
        return project_list;
    
    def schemes(self):
        """
        This method returns a list of schemes contained by the root project or workspace,
        as well as all referenced projects and workspaces. 
        """
        project_schemes = [];
        if self.isValid():
            for project_file in self.projects():
                for scheme in project_file.schemes():
                    project_schemes.append(scheme);
        return project_schemes;
    
    def findSchemeWithName(self, scheme_name):
        """
        This method returns a list of schemes with matching names to the passed name. List 
        items are tuples with the following elements:
        
        First element:
            A 'True' or 'False' value that indicates if a scheme was found
        
        Second element:
            'xcscheme' object of the scheme with matching name
        
        Third element:
            The container object for the scheme, either 'xcodeproj' or 'xcworkspace'
        """
        if self.isValid():
            results = map(lambda project: project.hasSchemeWithName(scheme_name) + (project,), self.projects());
            results = filter(lambda result: result[0] == True, results);
            if len(results) > 0:
                return results;
        return [(False, None, None)];