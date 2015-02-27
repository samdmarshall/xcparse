from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *

class PBXTargetDependency(object):
    # target = {};
    # proxy = {};
    
    def __init__(self, lookup_func, dictionary, project):
        if 'target' in dictionary.keys():
            result = lookup_func(project.objects()[dictionary['target']]);
            if result[0] == True:
                self.target = result[1](lookup_func, project.objects()[dictionary['target']], project);
        if 'targetProxy' in dictionary.keys():
            result = lookup_func(project.objects()[dictionary['targetProxy']]);
            if result[0] == True:
                self.target = result[1](lookup_func, project.objects()[dictionary['targetProxy']], project);