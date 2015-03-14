from ...Helpers import xcrun_helper

USE_XCODE_BUILD = 0;

class Base_Action(object):
    
    def __init__(self, action_xml):
        self.root = {};
        self.contents = action_xml;
    
    def performAction(self, build_system, container, xcparse_object, scheme_config_settings):
        """
        build_system = xcbuildsystem object - create with `xcbuildsystem()`
        container = xcscheme object - scheme that is having an action performed
        xcparse_object = xcparse object
        scheme_config_settings = dictionary containing any additional environment variables to set
        """
        print 'implement me!';