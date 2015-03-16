from ...Helpers import xcrun_helper
from .Base_Action import *

class AnalyzeAction(Base_Action):
    
    def __init__(self, action_xml):
        self.root = {};
        self.contents = action_xml;
        if 'buildConfiguration' in self.contents.keys():
            self.buildConfiguration = self.contents.get('buildConfiguration');
    
    def performAction(self, container, xcparse_object, configuration_name, additional_settings):
        """
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
                    xcrun_helper.perform_xcodebuild(project, container[1].name, 'analyze', additional_settings);
                else:
                    print 'implement me!';