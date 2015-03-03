from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBX_Base import *
from ..xcconfig import *

class XCBuildConfiguration(PBX_Base):
    # buildSettings = {};
    # name = '';
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'baseConfigurationReference' in dictionary.keys():
            self.baseConfigurationReference = self.parseProperty('baseConfigurationReference', lookup_func, dictionary, project, False);
        else:
            self.baseConfigurationReference = None;
        if 'buildSettings' in dictionary.keys():
            self.buildSettings = dictionary['buildSettings'];
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        
        # parse the xcconfig file
        if self.baseConfigurationReference != None:
            self.xcconfig = xcconfig(self.baseConfigurationReference.fs_path);
        else:
            # this needs to find the base config on the target
            self.xcconfig = xcconfig(None);
    
    def buildSettingForKey(self, key):
        if self.xcconfig != None:
            return self.xcconfig.valueForKey(key);
        return None;