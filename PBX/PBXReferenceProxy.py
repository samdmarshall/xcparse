from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBX_Base import *

class PBXReferenceProxy(PBX_Base):
    # fileType = '';
    # path = '';
    # sourceTree = '';
    # remoteRef = {};
    
    def __init__(self, lookup_func, dictionary, project):
        self.containerPortal = project.rootObject();
        if 'fileType' in dictionary.keys():
            self.fileType = dictionary['fileType'];
        if 'path' in dictionary.keys():
            self.path = dictionary['path'];
        if 'sourceTree' in dictionary.keys():
            self.sourceTree = dictionary['sourceTree'];
        if 'remoteRef' in dictionary.keys():
            self.remoteRef = self.parseProperty('remoteRef', lookup_func, dictionary, project, False);