from __future__ import absolute_import
import Cocoa
import Foundation
import os

from ..Path import *
from .PBXResolver import *
from .PBX_Base import *

class PBX_Base_Reference(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.name = 'PBX_BASE_REFERENCE';
        self.identifier = identifier;
        self.fs_path = None;
    
    # Absolute Path = <absolute>
    def resolveAbsolutePath(self, project, parent_path):
        return Path(self.path.obj_path, '');
    
    # Relative to Group = <group>
    def resolveGroupPath(self, project, parent_path):
        obj_path = '';
        if self.path != None:
            obj_path = self.path.obj_path;
        return Path(os.path.join(parent_path, obj_path), '');
    
    # Relative to Project = SOURCE_ROOT
    def resolveSourceRootPath(self, project, parent_path):
        obj_path = '';
        if self.path != None:
            obj_path = self.path.obj_path;
        return Path(os.path.join(project.projectRoot.obj_path, obj_path), '');
    
    # Relative to Developer Directory = DEVELOPER_DIR
    def resolveDeveloperDirPath(self, project, parent_path):
        obj_path = '';
        print 'FIND DEVELOPER_DIR';
        return Path(os.path.join(parent_path, obj_path), '');
    
    # Relative to Build Products = BUILT_PRODUCTS_DIR
    def resolveBuildProductsPath(self, project, parent_path):
        obj_path = '';
        print 'FIND BUILT_PRODUCTS_DIR';
        return Path(os.path.join(parent_path, obj_path), '');
    
    # Relative to SDK = SDKROOT
    def resolveSDKPath(self, project, parent_path):
        obj_path = '';
        print 'FIND SDKROOT';
        return Path(os.path.join(parent_path, obj_path), '');
    
    def lookupPathType(self, action_name):
        lookup = {
            '<absolute>': self.resolveAbsolutePath,
            '<group>': self.resolveGroupPath,
            'SOURCE_ROOT': self.resolveSourceRootPath,
            'DEVELOPER_DIR': self.resolveDeveloperDirPath,
            'BUILT_PRODUCTS_DIR': self.resolveBuildProductsPath,
            'SDKROOT': self.resolveSDKPath
        };
        if action_name in lookup.keys():
            return lookup[action_name];
        else:
            return None;
        
    def resolvePath(self, project, parent_path):
        action = self.lookupPathType(self.sourceTree);
        if action != None:
            self.fs_path = action(project, parent_path.obj_path);
            
            if hasattr(self, 'children'):
                self.children = list(map(lambda child: child.resolvePath(project, self.fs_path), self.children));
        