from __future__ import absolute_import

from ..xcrun import *

class AnalyzeAction(object):
    # contents = {};
    # children = [];
    # buildConfiguration = '';
    
    def __init__(self, action_xml):
        self.root = {};
        self.contents = action_xml;
        if 'buildConfiguration' in self.contents.keys():
            self.buildConfiguration = self.contents.get('buildConfiguration');
    
    def performAction(self, container, project_constructor, scheme_config_settings):
        if self.root != {}:
            for child in self.root.children:
                project_path = xcrun.resolvePathFromLocation(child.target.ReferencedContainer, container[2].path.base_path, container[2].path.base_path);
                project = project_constructor(project_path);
                
                xcrun.perform_xcodebuild(project, container[1].name, 'analyze', scheme_config_settings);