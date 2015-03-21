import os
from ...Helpers import xcrun_helper
from ...Helpers import path_helper
from .PBX_Base import *
from .PBX_Constants import *

class PBX_Base_Reference(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBX_Base_Reference, self).__init__(lookup_func, dictionary, project, identifier);
        self.fs_path = None;
        self.fs_found = False;
        
        self.path = None;
        if kPBX_REFERENCE_path in dictionary.keys():
            self.path = path_helper(dictionary[kPBX_REFERENCE_path], '');
            self.name = os.path.basename(self.path.obj_path);
        
        if kPBX_REFERENCE_name in dictionary.keys():
            self.name = dictionary[kPBX_REFERENCE_name];
        
        if kPBX_REFERENCE_refType in dictionary.keys():
            self.refType = dictionary[kPBX_REFERENCE_refType];
        
        if kPBX_REFERENCE_sourceTree in dictionary.keys():
            self.sourceTree = dictionary[kPBX_REFERENCE_sourceTree];
    
    # Absolute Path = <absolute>
    def resolveAbsolutePath(self, project, parent_path):
        return path_helper(self.path.obj_path, '');
    
    # Relative to Group = <group>
    def resolveGroupPath(self, project, parent_path):
        obj_path = '';
        if self.path != None:
            obj_path = self.path.obj_path;
        return path_helper(os.path.join(parent_path, obj_path), '');
    
    # Relative to Project = SOURCE_ROOT
    def resolveSourceRootPath(self, project, parent_path):
        obj_path = '';
        if self.path != None:
            obj_path = self.path.obj_path;
        return path_helper(os.path.join(project.projectRoot.obj_path, obj_path), '');
    
    # Relative to Developer Directory = DEVELOPER_DIR
    def resolveDeveloperDirPath(self, project, parent_path):
        developer_dir = xcrun_helper.resolve_developer_path();
        obj_path = '';
        if self.path != None:
            obj_path = self.path.obj_path;
        return path_helper(os.path.join(developer_dir, obj_path), '');
    
    # Relative to Build Products = BUILT_PRODUCTS_DIR
    def resolveBuildProductsPath(self, project, parent_path):
        target = project.targetForProductRef(self.identifier);
        if len(target) > 0:
            target = target[0];
        else:
            target = project;
        default_config = target.buildConfigurationList.defaultBuildConfiguration();
        symroot_path = default_config.buildSettingForKey('CONFIGURATION_BUILD_DIR');
        # default for now
        symroot_path = 'build'; 
        build_location = xcrun_helper.BuildLocation(project, symroot_path);
        obj_path = '';
        if self.path != None:
            obj_path = self.path.obj_path;
            # this should change to be the correct CONFIGURATION_BUILD_DIR path
        return path_helper(os.path.join(build_location, obj_path), '');
    
    # Relative to SDK = SDKROOT
    def resolveSDKPath(self, project, parent_path):
        target = project.targetForProductRef(self.identifier);
        if len(target) > 0:
            target = target[0];
        else:
            target = project;
        default_config = target.buildConfigurationList.defaultBuildConfiguration();
        sdk_path = xcrun_helper.resolve_sdk_path(default_config.buildSettingForKey('SDKROOT'));
        obj_path = '';
        if self.path != None:
            obj_path = self.path.obj_path;
        return path_helper(os.path.join(sdk_path, obj_path), '');
    
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
            self.fs_found = os.path.exists(self.fs_path.obj_path);
            
            if hasattr(self, kPBX_REFERENCE_children):
                self.children = list(map(lambda child: child.resolvePath(project, self.fs_path), self.children));
        