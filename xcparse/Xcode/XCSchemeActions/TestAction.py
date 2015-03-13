from ...Helpers import xcrun_helper
from .Base_Action import *

class TestAction(Base_Action):
    
    def __init__(self, action_xml):
        self.root = {};
        self.contents = action_xml;
        if 'selectedDebuggerIdentifier' in self.contents.keys():
            self.selectedDebuggerIdentifier = self.contents.get('selectedDebuggerIdentifier');
        if 'selectedLauncherIdentifier' in self.contents.keys():
            self.selectedLauncherIdentifier = self.contents.get('selectedLauncherIdentifier');
        if 'shouldUseLaunchSchemeArgsEnv' in self.contents.keys():
            self.shouldUseLaunchSchemeArgsEnv = self.contents.get('shouldUseLaunchSchemeArgsEnv');
        if 'buildConfiguration' in self.contents.keys():
            self.buildConfiguration = self.contents.get('buildConfiguration');
    
    def performAction(self, build_system, container, xcparse_object, scheme_config_settings):
        """
        build_system = xcbuildsystem object - create with `xcbuildsystem()`
        container = xcscheme object - scheme that is having an action performed
        xcparse_object = xcparse object
        scheme_config_settings = dictionary containing any additional environment variables to set
        """
        if self.root != {}:
            for child in self.root.children:
                project_path = xcrun_helper.resolvePathFromLocation(child.target.ReferencedContainer, container[2].path.base_path, container[2].path.base_path);
                project = filter(lambda proj: proj.path.obj_path == project_path, xcparse_object.projects());
                if len(project) > 0:
                    project = project[0];
                else:
                    project = xcparse_object.project_constructor(project_path);
                
                if USE_XCODE_BUILD == 1:
                    xcrun_helper.perform_xcodebuild(project, container[1].name, 'test', scheme_config_settings);
                else:
                    print 'implement me!';