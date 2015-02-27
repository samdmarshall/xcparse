from __future__ import absolute_import
import Cocoa
import Foundation
import os

class PBXFileReference(object):
    # name = '';
    # path = '';
    # ftype = '';
    # sourceTree = '';
    
    def __init__(self, lookup_func, dictionary, project):
        if 'path' in dictionary.keys():
            self.path = dictionary['path'];
            self.name = os.path.basename(self.path);
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];
        if 'lastKnownFileType' in dictionary.keys():
            self.ftype = dictionary['lastKnownFileType'];
        if 'sourceTree' in dictionary.keys():
            self.sourceTree = dictionary['sourceTree'];