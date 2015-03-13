from ...Helpers import xcrun_helper
from .Base_Action import *

class AnalyzeAction(Base_Action):
    # contents = {};
    # children = [];
    # buildConfiguration = '';
    
    def __init__(self, action_xml):
        self.root = {};
        self.contents = action_xml;
        if 'buildConfiguration' in self.contents.keys():
            self.buildConfiguration = self.contents.get('buildConfiguration');
    
    def performAction(self, build_system, container, project_constructor, scheme_config_settings):
        if self.root != {}:
            for child in self.root.children:
                project_path = xcrun_helper.resolvePathFromLocation(child.target.ReferencedContainer, container[2].path.base_path, container[2].path.base_path);
                project = project_constructor(project_path);
                
                xcrun_helper.perform_xcodebuild(project, container[1].name, 'analyze', scheme_config_settings);