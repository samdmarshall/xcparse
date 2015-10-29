from __future__ import absolute_import
import os
import sys

class xcspec(object):
    
    def __init__(self, spec_data):
        self.contents = spec_data;
        self.identifier = '';
        self.type = '';
        self.name = '';
        self.basedOn = None;
        if 'Identifier' in self.keys():
            self.identifier = str(self.contents['Identifier']);
        if 'Type' in self.keys():
            self.type = str(self.contents['Type']);
        if 'Name' in self.keys():
            self.name = str(self.contents['Name']);
        if 'BasedOn' in self.keys():
            self.basedOn = str(self.contents['BasedOn']);
    
    def __attrs(self):
        return (self.identifier, self.type);
    
    def __repr__(self):
        return '(%s : %s : %s)' % (type(self), self.name, self.identifier);
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.identifier == other.identifier and self.type == other.type;
    
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