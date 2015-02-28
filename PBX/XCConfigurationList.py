from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base import *

class XCConfigurationList(PBX_Base):
    # buildConfigurations = [];
    # defaultConfigurationIsVisible = 0;
    # defaultConfigurationName = '';
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'buildConfigurations' in dictionary.keys():
            self.buildConfigurations = self.parseProperty('buildConfigurations', lookup_func, dictionary, project, True);
        if 'defaultConfigurationName' in dictionary.keys():
            self.defaultConfigurationName = dictionary['defaultConfigurationName'];
        if 'defaultConfigurationIsVisible' in dictionary.keys():
            self.defaultConfigurationIsVisible = dictionary['defaultConfigurationIsVisible'];