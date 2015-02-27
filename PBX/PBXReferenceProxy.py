from __future__ import absolute_import
import Cocoa
import Foundation
import os

class PBXReferenceProxy(object):
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
            result = lookup_func(project.objects()[dictionary['remoteRef']])
            if result[0] == True:
                self.remoteRef = result[1](lookup_func, project.objects()[dictionary['remoteRef']], project);