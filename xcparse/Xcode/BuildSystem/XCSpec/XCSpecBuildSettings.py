from __future__ import absolute_import
import os
import sys

from .xcspec import *

class XCSpecBuildSettings(xcspec):
    
    def __init__(self, spec_data):
        super(XCSpecBuildSettings, self).__init__(spec_data);