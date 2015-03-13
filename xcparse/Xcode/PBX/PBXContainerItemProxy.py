from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBX_Base import *

class PBXContainerItemProxy(PBX_Base):
    # containerPortal = {};
    # proxyType = 0;
    # remoteGlobalIDString = '';
    # remoteInfo = '';
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        if 'containerPortal' in dictionary.keys():
            self.containerPortal = dictionary['containerPortal'];
        if 'proxyType' in dictionary.keys():
            self.proxyType = dictionary['proxyType'];
        if 'remoteGlobalIDString' in dictionary.keys():
            self.remoteGlobalIDString = dictionary['remoteGlobalIDString'];
        if 'remoteInfo' in dictionary.keys():
            self.remoteInfo = dictionary['remoteInfo'];