from ...Helpers import xcrun_helper

USE_XCODE_BUILD = 0;

class Base_Action(object):
    
    def __init__(self, action_xml):
        self.root = {};
        self.contents = action_xml;
    
    def performAction(self, container, xcparse_object, configuration_name, additional_settings):
        """
        container = xcscheme object - scheme that is having an action performed
        xcparse_object = xcparse object
        scheme_config_settings = dictionary containing any additional environment variables to set
        """
        print 'implement me!';