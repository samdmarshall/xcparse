from __future__ import absolute_import
import Cocoa
import Foundation
import os

class PBXContainerItemProxy(object):
    # containerPortal = {};
    # proxyType = 0;
    # remoteGlobalIDString = '';
    # remoteInfo = '';
    
    def __init__(self, lookup_func, dictionary, project):
        self.containerPortal = project.rootObject();
        if 'proxyType' in dictionary.keys():
            self.proxyType = dictionary['proxyType'];
        if 'remoteGlobalIDString' in dictionary.keys():
            self.remoteGlobalIDString = dictionary['remoteGlobalIDString'];
        if 'remoteInfo' in dictionary.keys():
            self.remoteInfo = dictionary['remoteInfo'];