from __future__ import absolute_import
import os
import sys

from .xcspec import *

class XCSpecBuildStep(xcspec):
    
    def __init__(self, spec_data):
        super(XCSpecBuildStep, self).__init__(spec_data);