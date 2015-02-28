from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base_Target import *

class PBXAggregateTarget(PBX_Base_Target):
    # buildConfigurationList = {};
    # buildPhases = [];
    # dependencies = [];
    # name = '';
    # productName = '';
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        if 'productName' in dictionary.keys():
            self.productName = dictionary['productName'];
        if 'buildConfigurationList' in dictionary.keys():
            self.buildConfigurationList = self.parseProperty('buildConfigurationList', lookup_func, dictionary, project, False);
        if 'buildPhases' in dictionary.keys():
            self.buildPhases = self.parseProperty('buildPhases', lookup_func, dictionary, project, True);
        if 'dependencies' in dictionary.keys():
            self.dependencies = self.parseProperty('dependencies', lookup_func, dictionary, project, True);