from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBXSourcesBuildPhase import *
from .PBXFrameworksBuildPhase import *

class PBX_Base_Target(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project):
        self.name = 'PBX_BASE_TARGET';
        self.buildPhases = [];
    
    def resolve(self, type, list):
        return filter(lambda item: isinstance(item, type), list);
    
    def sourceFiles(self):
        file_list = [];
        source_phase_list = self.resolve(PBXSourcesBuildPhase, self.buildPhases);
        for phase in source_phase_list:
            file_list.extend(phase.files);
        return file_list;
    
    def linkedLibraries(self):
        library_list = [];
        framework_phase_list = self.resolve(PBXFrameworksBuildPhase, self.buildPhases);
        for phase in framework_phase_list:
            library_list.extend(phase.files);
        return library_list;