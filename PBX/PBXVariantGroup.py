from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base import *

class PBXVariantGroup(PBX_Base):
    # name = '';
    # path = '';
    # children = [];
    
    def __init__(self, lookup_func, dictionary, project):
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        if 'path' in dictionary.keys():
            self.path = dictionary['path'];
        if 'children' in dictionary.keys():
            self.children = self.parseProperty('children', lookup_func, dictionary, project, True);