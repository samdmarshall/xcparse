from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *

class PBXBuildFile(object):
    # fileRef = {};
    
    def __init__(self, lookup_func, dictionary, project):
        if 'fileRef' in dictionary.keys():
            result = lookup_func(project.objects()[dictionary['fileRef']]);
            if result[0] == True:
                self.fileRef = result[1](lookup_func, project.objects()[dictionary['fileRef']], project)