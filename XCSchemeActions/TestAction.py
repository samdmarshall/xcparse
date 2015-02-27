from __future__ import absolute_import

from ..xcrun import *

class TestAction(object):
    # contents = {};
    # children = [];
    # selectedDebuggerIdentifier = '';
    # selectedLauncherIdentifier = '';
    # shouldUseLaunchSchemeArgsEnv = '';
    # buildConfiguration = '';
    
    
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
    
    def performAction(self, container, project_constructor, scheme_config_settings):
        if self.root != {}:
            for child in self.root.children:
                project_path = xcrun.resolvePathFromLocation(child.target.ReferencedContainer, container[2].path.base_path, container[2].path.base_path);
                project = project_constructor(project_path);
                
                xcrun.perform_xcodebuild(project, container[1].name, 'test', scheme_config_settings);