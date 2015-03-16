import xml.etree.ElementTree as xml
from xcodeproj import xcodeproj
from ..Helpers import path_helper
from ..Helpers import xcrun_helper
from xc_base import xc_base
from ..Helpers import logging_helper

class xcworkspace(xc_base):
    
    def __init__(self, xcworkspace_path):
        """
        Pass the path to a 'xcworkspace' file to initialize the xcworkspace object.
        """
        self.data = None;
        if xcworkspace_path.endswith('.xcworkspace'):
            self.path = path_helper(xcworkspace_path, 'contents.xcworkspacedata');
            
            if os.path.exists(self.path.root_path) == True:
                try:
                    self.data = xml.parse(self.path.root_path);
                except:
                    self.data = None;
            else:
                logging_helper.getLogger().error('[xcworkspace]: Could not find xcworkspacedata file!');
        else:
            logging_helper.getLogger().error('[xcworkspace]: Invalid xcworkspace file!');
    
    def isValid(self):
        return self.data != None;
    
    def __resolvePathFromXMLItem(self, node, path):
        path = None;
        if self.isValid():
            file_relative_path = node.attrib['location'];
            path = xcrun_helper.resolvePathFromLocation(file_relative_path, path, self.path.base_path);
        return path;
    
    def __parsePathsFromXMLItem(self, node, path):
        results = [];
        if self.isValid():
            item_path = self.__resolvePathFromXMLItem(node, path);
            if node.tag == 'FileRef':
                if os.path.exists(item_path) == True:
                    project_parse = xcodeproj(item_path);
                    if project_parse.isValid() == True:
                        results.append(project_parse);
            if node.tag == 'Group':
                path = os.path.join(path, item_path);
                for child in node:
                    group_results = self.__parsePathsFromXMLItem(child, path);
                    for item in group_results:
                        results.append(item);
        return results;
    
    def projects(self):
        """
        This will return a list of projects referenced in this workspace.
        """
        indexed_projs = [];
        if self.isValid():
            workspace_base_path = self.path.base_path;
            workspace_root = self.data.getroot();
            for child in workspace_root:
                results = self.__parsePathsFromXMLItem(child, workspace_base_path);
                for item in results:
                    indexed_projs.append(item);
        return indexed_projs;
    