import xml.etree.ElementTree as xml
from ...Helpers import xcrun_helper
from ..PBX import PBXResolver
from ..PBX.PBX_Constants import *
from ..BuildSystem import xcbuildsystem
from .Base_Action import *
from .BuildActionEntry import *
from ...Helpers import logging_helper
import os

class BuildAction(Base_Action):
    
    def __init__(self, action_xml):
        self.contents = action_xml;
        if 'parallelizeBuildables' in self.contents.keys():
            self.parallel = self.contents.get('parallelizeBuildables');
        if 'buildImplicitDependencies' in self.contents.keys():
            self.implicit = self.contents.get('buildImplicitDependencies');
        self.children = list(map(lambda entry: BuildActionEntry(entry), list(self.contents.find('./BuildActionEntries'))));
        
    def performAction(self, container, xcparse_object, configuration_name, additional_settings):
        """
        build_system = xcbuildsystem object - create with `xcbuildsystem()`
        container = xcscheme object - scheme that is having an action performed
        xcparse_object = xcparse object
        scheme_config_settings = dictionary containing any additional environment variables to set
        """
        # iterate over the BuildActionEnties in the BuildAction
        for child in self.children:
            # based on the reference to the project container, get the project file path
            project_path = xcrun_helper.resolvePathFromLocation(child.target.ReferencedContainer, container[2].path.base_path, container[2].path.base_path);
            # getting the xcodeproj object for the child dependency
            project = filter(lambda proj: proj.path.obj_path == project_path, xcparse_object.projects());
            if len(project) > 0:
                project = project[0];
            else:
                # if it isn't part of the xcparse object for some reason, make a new project object
                project = xcparse_object.project_constructor(project_path);
            
            # this is a conditional for testing purposes, eventually this check and dispatch to xcodebuild will go away
            if USE_XCODE_BUILD == 1:
                # using the xcode build system
                xcrun_helper.perform_xcodebuild(project, container[1].name, 'build', additional_settings);
            else:
                # using the xcparse build system
                self.buildTarget(project, configuration_name, child.target.BlueprintIdentifier);
        
    def buildTarget(self, project, configuration_name, target_identifier):
        """
        This method dispatches building a target in a project file.
        
        project = xcodeproj object - taken from BuildAction.performAction()
        target_identifier = string identifier of the object in the xcodeproj file
        """
        # check to make sure that the target is a valid dependency
        if target_identifier in project.contents[kPBX_objects].keys():
            # get the target from the project file
            target = filter(lambda target: target.identifier == target_identifier, project.targets());
            if len(target) > 0:
                target = target[0];
            else:
                logging_helper.getLogger().error('[BuildAction]: Could not find a target with identifier "%s" in project "%s"' % (target_identifier, project.path.root_path));
            
            # make sure that the project was found
            if target != None:
                print target.name;
                print '========================';
            
                # building any explicit dependencies first
                for dependent in target.dependencies:
                    self.buildTarget(project, configuration_name, dependent.proxy.remoteGlobalIDString);
            
                # create a new build system environment for this target to build in
                build_system = xcbuildsystem();
                # setting up environment first, cannot rely on build phase ordering to initialize this first
                build_system.initEnvironment(project, configuration_name);
                build_system.environment.setValueForKey('ACTION', 'build', {});
                build_system.environment.setValueForKey('BUILD_COMPONENTS', build_system.environment.getBuildComponents(), {});
                build_system.environment.setValueForKey('TARGET_NAME', target.name, {}, 'target');
                build_system.environment.setValueForKey('TARGETNAME', target.name, {}, 'target');
                build_system.environment.setValueForKey('PRODUCT_NAME', target.productName, {});
                # setting the project level build environment
                project_build_settings = project.rootObject.buildConfigurationList.buildConfigurationWithName(configuration_name).buildSettings;
                for setting in project_build_settings.keys():
                    build_system.environment.setValueForKey(setting, project_build_settings[setting], {}, 'project');
                # setting the target level build environment
                target_build_config = target.buildConfigurationList.buildConfigurationWithName(configuration_name);
                target_build_settings = target_build_config.buildSettings;
                for setting in target_build_settings.keys():
                    build_system.environment.setValueForKey(setting, target_build_settings[setting], {}, 'target');
                # setting the config level build environment
                config_build_settings = target_build_config.xcconfig;
                if config_build_settings != None:
                    build_system.environment.applyConfig(config_build_settings);
                # setting the defaults
                build_system.environment.loadDefaults();
                
                # this loads the platform target and package types
                platform_specs_path = os.path.join(build_system.environment.valueForKey('PLATFORM_DIR'), 'Developer/Library/Xcode/Specifications');
                build_system.loadSpecsAtPath(platform_specs_path);
                
                # getting the target type from the target
                if hasattr(target, kPBX_TARGET_productType):
                    # locating the target type spec to load the default build settings from it
                    target_spec = build_system.getSpecForIdentifier(target.productType);
                    for setting in target_spec.contents['DefaultBuildProperties'].keys():
                        build_system.environment.setValueForKey(setting, target_spec.contents['DefaultBuildProperties'][setting], {}, 'target');
                    
                    # locating the package type spec to load the default build settings
                    package_spec = build_system.getSpecForIdentifier(str(target_spec.contents['PackageTypes'][0]));
                    for setting in package_spec.contents['DefaultBuildSettings'].keys():
                        build_system.environment.setValueForKey(setting, package_spec.contents['DefaultBuildSettings'][setting], {}, 'target');
                
                # running build phases for this target
                target.executeBuildPhases(build_system);
                