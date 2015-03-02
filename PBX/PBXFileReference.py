from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBX_Base_Reference import *
from ..Path import *

class PBXFileReference(PBX_Base_Reference):
    # name = '';
    # path = '';
    # ftype = '';
    # sourceTree = '';
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        self.path = None;
        self.fs_path = None;
        if 'path' in dictionary.keys():
            self.path = Path(dictionary['path'], '');
            self.name = os.path.basename(self.path.base_path);
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