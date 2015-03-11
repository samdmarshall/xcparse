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
    if os.path.exists(xcspec_path) == True:
        return xcspecLoadFromContentsAtPath(xcspec_path);
    else:
        return [];

def xcspecLoadFromContentsAtPath(spec_path):
    contents = None;
    if spec_path.endswith('spec'):
        path = Path(spec_path, '');
        
        if os.path.exists(path.root_path) == True:
            # loading spec file
            specNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(path.root_path, Foundation.NSUncachedRead, None);
            if errorMessage == None:
                specString = Foundation.NSString.alloc().initWithData_encoding_(specNSData, Foundation.NSUTF8StringEncoding);
                if specString != None:
                    contents = specString.propertyList();
                else:
                    print 'Could not load string from data';
            else:
                print errorMessage;
        else:
            print 'Path does not exist!';
    else:
        print 'Not a xcspec file!';
    
    items = [];
    
    if contents != None:
        if hasattr(contents, 'keys'):
            items.append(xcspec(contents));
        else:
            for spec_item in contents:
                items.append(xcspec(spec_item));
    
    return items;

class xcspec(object):
    
    def __init__(self, spec_data):
        self.contents = spec_data;
        self.identifier = '';
        self.type = '';
        self.name = '';
        self.basedOn = None;
        if 'Identifier' in self.keys():
            self.identifier = self.contents['Identifier'];
        if 'Type' in self.keys():
            self.type = self.contents['Type'];
        if 'Name' in self.keys():
            self.name = self.contents['Name'];
        if 'BasedOn' in self.keys():
            self.basedOn = self.contents['BasedOn'];
    
    def __attrs(self):
        return (self.identifier);
    
    def __repr__(self):
        return '%s : %s : %s' % (type(self), self.name, self.identifier);
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.identifier == other.identifier;
    
    def __hash__(self):
        return hash(self.__attrs());
    
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
            return [];
    
    def valueForKey(self, key):
        value = None;
        if not self.isValid():
            return value;
        if self.hasKeys():
            value = self.contents[key];
        
        return value;
    
    def inheritedTypes(self):
        types = [str(self.identifier)];
        if self.basedOn != None:
            parent = self.basedOn.inheritedTypes();
            types.extend(parent);
        return types;