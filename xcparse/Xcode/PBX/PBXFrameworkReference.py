from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBX_Base_Reference import *

class PBXFrameworkReference(PBX_Base_Reference):
    # name = string
    # path = string
    # reftype = int
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        self.fs_path = None;
        self.path = None;
        if 'path' in dictionary.keys():
            self.path = Path(dictionary['path'], '');
            self.name = os.path.basename(self.path.obj_path);
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        if 'refType' in dictionary.keys():
            self.refType = dictionary['refType'];
        if 'sourceTree' in dictionary.keys():
            self.sourceTree = dictionary['sourceTree'];