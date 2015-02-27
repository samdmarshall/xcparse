from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *

class PBXAggregateTarget(object):
    # buildConfigurationList = {};
    # buildPhases = [];
    # dependencies = [];
    # name = '';
    # productName = '';
    
    def __init__(self, lookup_func, dictionary, project):
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        if 'productName' in dictionary.keys():
            self.productName = dictionary['productName'];
        if 'buildConfigurationList' in dictionary.keys():
            result = lookup_func(project.objects()[dictionary['buildConfigurationList']])
            if result[0] == True:
                self.buildConfigurationList = result[1](lookup_func, project.objects()[dictionary['buildConfigurationList']], project);
        if 'buildPhases' in dictionary.keys():
            phaseList = [];
            for phase in dictionary['buildPhases']:
                result = lookup_func(project.objects()[phase]);
                if result[0] == True:
                    result = result[1](lookup_func, project.objects()[phase], project);
                    phaseList.append(result);
            self.buildPhases = phaseList;
        if 'dependencies' in dictionary.keys():
            dependencies = [];
            for dep in dictionary['dependencies']:
                # this may need to be changed to PBXTargetDependency
                dependencies.append(dep);
            self.dependencies = dependencies;