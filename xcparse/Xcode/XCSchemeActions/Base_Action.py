from ...Helpers import xcrun_helper

class Base_Action(object):
    
    def __init__(self, action_xml):
        self.root = {};
        self.contents = action_xml;
    
    def performAction(self, build_system, container, project_constructor, scheme_config_settings):
        print 'implement me!';