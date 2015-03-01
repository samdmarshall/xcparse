from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBX_Base import *

class PBXZipArchiveReference(PBX_Base):
    # path = string
    # reftype = int
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'path' in dictionary.keys():
            self.path = dictionary['path'];
            self.name = os.path.basename(self.path);
        if 'refType' in dictionary.keys():
            self.refType = dictionary['refType'];