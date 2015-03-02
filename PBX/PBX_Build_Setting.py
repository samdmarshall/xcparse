from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *

class PBX_Build_Setting(object):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.name = 'PBX_BUILD_SETTING';
        self.identifier = identifier;
    
    def buildSettings(self, configuration_name):
        """
        This method will return a dictionary of build settings for the level of the object
        """
        settings = {};
        #if hasattr(self, 'buildConfigurationList'):
            
        return settings;