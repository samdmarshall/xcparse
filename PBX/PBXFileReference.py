from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBX_Base import *

class PBXFileReference(PBX_Base):
    # name = '';
    # path = '';
    # ftype = '';
    # sourceTree = '';
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'path' in dictionary.keys():
            self.path = dictionary['path'];
            self.name = os.path.basename(self.path);
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        if 'lastKnownFileType' in dictionary.keys():
            self.ftype = dictionary['lastKnownFileType'];
        if 'sourceTree' in dictionary.keys():
            self.sourceTree = dictionary['sourceTree'];
        if 'fileEncoding' in dictionary.keys():
            self.fileEncoding = dictionary['fileEncoding'];
        if 'explicitFileType' in dictionary.keys():
            self.explicitFileType = dictionary['explicitFileType'];
        if 'includeInIndex' in dictionary.keys():
            self.includeInIndex = dictionary['includeInIndex'];