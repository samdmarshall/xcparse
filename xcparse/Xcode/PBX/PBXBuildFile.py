from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base import *

class PBXBuildFile(PBX_Base):
    # fileRef = {};
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        self.name = '';
        if 'fileRef' in dictionary.keys():
            self.fileRef = self.parseProperty('fileRef', lookup_func, dictionary, project, False);
            self.name = self.fileRef.name;
        if 'settings' in dictionary.keys():
            self.settings = dictionary['settings'];