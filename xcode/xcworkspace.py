from __future__ import absolute_import
import xml.etree.ElementTree as xml
import os
import sys

from ..Path import *
from ..Logger import *

from .xcodeproj import *
from .xcrun import *
from .xcscheme import *

class xcworkspace(object):
    # path = {};
    # data = {};
    
    def __init__(self, xcworkspace_path):
        self.path = Path(xcworkspace_path, 'contents.xcworkspacedata');
        
        if os.path.exists(self.path.root_path) == True:
            try:
                self.data = xml.parse(self.path.root_path);
            except:
                self.data = {};
        else:
            Logger.debuglog([
                            Logger.colour('red',True),
                            Logger.string('%s', 'Invalid xcworkspace file!'),
                            Logger.colour('reset', True)
                            ]);
    
    def isValid(self):
        return self.data != {};
    
    def resolvePathFromXMLItem(self, node, path):
        file_relative_path = node.attrib['location'];
        result = xcrun.resolvePathFromLocation(file_relative_path, path, self.path.base_path);
        return result;
    
    def parsePathsFromXMLItem(self, node, path):
        results = [];
        item_path = self.resolvePathFromXMLItem(node, path);
        if node.tag == 'FileRef':
            if os.path.exists(item_path) == True:
                project_parse = xcodeproj(item_path);
                if project_parse.isValid() == True:
                    results.append(project_parse);
        if node.tag == 'Group':
            path = os.path.join(path, item_path);
            for child in node:
                group_results = self.parsePathsFromXMLItem(child, path);
                for item in group_results:
                    results.append(item);
        return results;
    
    def projects(self):
        indexed_projs = [];
        if self.data != '':
            workspace_base_path = self.path.base_path;
            workspace_root = self.data.getroot();
            for child in workspace_root:
                results = self.parsePathsFromXMLItem(child, workspace_base_path);
                for item in results:
                    indexed_projs.append(item);
        return indexed_projs;
    
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
        