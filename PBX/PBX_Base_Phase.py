from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBX_Base import *

class PBX_Base_Phase(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.name = 'PBX_BASE_PHASE';
        self.identifier = identifier;
        self.phase_type = 'BASE';
        
    def performPhase(self):
        print '%s Phase: implement me!' % (self.phase_type);