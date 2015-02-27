from __future__ import absolute_import
import Cocoa
import Foundation
import os

class XCBuildConfiguration(object):
    # buildSettings = {};
    # name = '';
    
    def __init__(self, lookup_func, dictionary, project):
        if 'buildSettings' in dictionary.keys():
            self.buildSettings = dictionary['buildSettings'];
        if 'name' in dictionary.keys():
            self.name = dictionary['name'];