from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *

class PBXVariantGroup(object):
    # name = '';
    # path = '';
    # children = [];
    
    def __init__(self, lookup_func, dictionary, project):
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        if 'path' in dictionary.keys():
            self.path = dictionary['path'];
        if 'children' in dictionary.keys():
            children = [];
            for child in dictionary['children']:
                result = lookup_func(project.objects()[child]);
                if result[0] == True:
                    children.append(result[1](lookup_func, project.objects()[child], project));
            self.children = children;