from __future__ import absolute_import
import os
import sys

from .xcspec import *

class XCSpecPackageType(xcspec):
    
    def __init__(self, spec_data):
        super(XCSpecPackageType, self).__init__(spec_data);