# this is going to be for loading the spec files.
from __future__ import absolute_import
import Cocoa
import Foundation
import os
import sys

from .Path import *

from .xcrun import *

class xcspec(object):
    
    def __init__(self, spec_path):
        self.path = None;
        self.contents = None;
        if spec_path.endswith('.xcspec'):
            self.path = Path(spec_path, '');
            
            if os.path.exists(self.path.root_path) == True:
                # loading spec file
                specNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(self.path.root_path, Foundation.NSUncachedRead, None);
                if errorMessage == None:
                    specString = Foundation.NSString.alloc().initWithData_encoding_(specNSData, Foundation.NSUTF8StringEncoding);
                    if specString != None:
                        self.contents = specString.propertyList();
                    else:
                        print 'Could not load string from data';
                else:
                    print errorMessage;
            else:
                print 'Path does not exist!';
        else:
            print 'Not a xcspec file!';
    
    def keys(self):
        return self.contents.keys();
    
    def valueForKey(self, key):
        value = None;
        if key in self.contents.keys():
            value = self.contents[key];
        else:
            keys = list(map(lambda item: item.name, self.contents));
            value = filter(lambda item: item.name == key, keys);
        return value;
                