from __future__ import absolute_import
import os
import sys

from .xcspec import *

class XCSpecCompiler(xcspec):
    
    def __init__(self, spec_data):
        self.contents = spec_data;
        self.identifier = '';
        self.type = '';
        self.name = '';
        self.basedOn = None;
        self.abstract = 'NO';
        if 'Identifier' in self.keys():
            self.identifier = self.contents['Identifier'];
        if 'Type' in self.keys():
            self.type = self.contents['Type'];
        if 'Name' in self.keys():
            self.name = self.contents['Name'];
        if 'BasedOn' in self.keys():
            self.basedOn = self.contents['BasedOn'];
        if 'IsAbstract' in self.keys():
            self.abstract = self.contents['IsAbstract'];