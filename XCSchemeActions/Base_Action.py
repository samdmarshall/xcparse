from __future__ import absolute_import

from ..xcrun import *

class Base_Action(object):
    
    def __init__(self, action_xml):
        self.root = {};
        self.contents = action_xml;
    
    def performAction(self, container, project_constructor, scheme_config_settings):
        print 'implement me!';