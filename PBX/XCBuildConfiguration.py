from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBX_Base import *

class XCBuildConfiguration(PBX_Base):
    # buildSettings = {};
    # name = '';
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'baseConfigurationReference' in dictionary.keys():
            self.baseConfigurationReference = dictionary['baseConfigurationReference'];
        if 'buildSettings' in dictionary.keys():
            self.buildSettings = dictionary['buildSettings'];
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];