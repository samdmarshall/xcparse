from __future__ import absolute_import
import os
import sys

from .xcspec import *

class XCSpecCompiler(xcspec):
    
    def __init__(self, spec_data):
        super(XCSpecCompiler, self).__init__(spec_data);
        self.abstract = 'NO';
        if 'IsAbstract' in self.keys():
            self.abstract = self.contents['IsAbstract'];