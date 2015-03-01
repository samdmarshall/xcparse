from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base_Target import *

class PBXLegacyTarget(PBX_Base_Target):
    # buildConfigurationList = {};
    # buildPhases = [];
    # dependencies = [];
    # name = '';
    # productName = '';
    # buildToolPath = '';
    # buildArgumentsString = '';
    # passBuildSettingsInEnvironment = 0;
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'buildSettings' in dictionary.keys():
            self.buildSettings = dictionary['buildSettings'];
        if 'buildConfigurationList' in dictionary.keys():
            self.buildConfigurationList = self.parseProperty('buildConfigurationList', lookup_func, dictionary, project, False);
        if 'buildPhases' in dictionary.keys():
            self.buildPhases = self.parseProperty('buildPhases', lookup_func, dictionary, project, True);
        if 'dependencies' in dictionary.keys():
            self.dependencies = self.parseProperty('dependencies', lookup_func, dictionary, project, True);
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        if 'productName' in dictionary.keys():
            self.productName = dictionary['productName'];
        if 'passBuildSettingsInEnvironment' in dictionary.keys():
            self.passBuildSettingsInEnvironment = dictionary['passBuildSettingsInEnvironment'];
        if 'buildArgumentsString' in dictionary.keys():
            self.buildArgumentsString = dictionary['buildArgumentsString'];
        if 'buildToolPath' in dictionary.keys():
            self.buildToolPath = dictionary['buildToolPath'];
        if 'buildWorkingDirectory' in dictionary.keys():
            self.buildWorkingDirectory = dictionary['buildWorkingDirectory'];
        if 'settingsToExpand' in dictionary.keys():
            self.settingsToExpand = dictionary['settingsToExpand'];
        if 'settingsToPassInEnvironment' in dictionary.keys():
            self.settingsToPassInEnvironment = dictionary['settingsToPassInEnvironment'];
        if 'settingsToPassOnCommandLine' in dictionary.keys():
            self.settingsToPassOnCommandLine = dictionary['settingsToPassOnCommandLine'];
        if 'shouldUseHeadermap' in dictionary.keys():
            self.shouldUseHeadermap = dictionary['shouldUseHeadermap'];