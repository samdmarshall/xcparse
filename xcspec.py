# this is going to be for loading the spec files.
from __future__ import absolute_import
import Cocoa
import Foundation
import os
import sys

from .Path import *

from .xcrun import *

def xcspecLoadFileAtRelativeDeveloperPath(path):
    xcspec_path = os.path.normpath(os.path.join(xcrun.resolve_developer_path(), path));
    return xcspec(xcspec_path);

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
    
    def isValid(self):
        return self.contents != None;
    
    def hasKeys(self):
        if self.isValid():
            return hasattr(self.contents, 'keys');
        else:
            return False;
    
    def keys(self):
        if not self.isValid():
            return [];
        if self.hasKeys():
            return self.contents.keys();
        else:
            return list(map(lambda item: item.name, self.contents));
    
    def valueForKey(self, key):
        value = None;
        if not self.isValid():
            return value;
        if self.hasKeys():
            value = self.contents[key];
        else:
            value = filter(lambda item: item.name == key, self.keys());
        return value;
                