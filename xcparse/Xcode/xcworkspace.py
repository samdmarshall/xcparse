import os
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
        self.identifier = '';
        self.contents = None;
        if xcworkspace_path.endswith('.xcworkspace'):
            self.path = path_helper(xcworkspace_path, 'contents.xcworkspacedata');
            self.identifier = os.path.basename(self.path.obj_path);
            if os.path.exists(self.path.root_path) == True:
                try:
                    self.contents = xml.parse(self.path.root_path);
                except:
                    logging_helper.getLogger().error('[xcworkspace]: Failed to load xcworkspacedata file!');
            else:
                logging_helper.getLogger().error('[xcworkspace]: Could not find xcworkspacedata file!');
        else:
            logging_helper.getLogger().error('[xcworkspace]: Invalid xcworkspace file!');
    
    def __resolvePathFromXMLItem(self, node, path):
        """
        This is a private method used to resolve the path location into a real filesystem path.
        """
        path = '';
        if self.isValid():
            file_relative_path = node.attrib['location'];
            path = xcrun_helper.resolvePathFromLocation(file_relative_path, path, self.path.base_path);
        return path;
    
    def __parsePathsFromXMLItem(self, node, path):
        """
        This is a private method used to parse each node in the xcworkspace xml file to get projects from the included file paths.
        """
        results = [];
        if self.isValid():
            item_path = self.__resolvePathFromXMLItem(node, path);
            if node.tag == 'FileRef':
                if os.path.exists(item_path) == True:
                    if item_path.endswith('.xcodeproj') or item_path.endswith('.pbproj'):
                        project_parse = xcodeproj(item_path);
                        if project_parse.isValid() == True:
                            results.append(project_parse);
            if node.tag == 'Group':
                path = os.path.join(path, item_path);
                for child in node:
                    results.extend(self.__parsePathsFromXMLItem(child, path));
        return results;
    
    def projects(self):
        """
        Returns a list of projects referenced in this workspace.
        """
        indexed_projs = [];
        if self.isValid():
            workspace_base_path = self.path.base_path;
            workspace_root = self.contents.getroot();
            for child in workspace_root:
                indexed_projs.extend(self.__parsePathsFromXMLItem(child, workspace_base_path));
        return indexed_projs;
    