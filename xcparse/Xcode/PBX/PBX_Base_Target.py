from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *
from .PBXSourcesBuildPhase import *
from .PBXFrameworksBuildPhase import *
from .PBX_Build_Setting import *

class PBX_Base_Target(PBX_Base, PBX_Build_Setting):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.name = 'PBX_BASE_TARGET';
        self.identifier = identifier;
        self.buildPhases = [];
        self.dependencies = [];
        self.productReference = '';
        self.buildRules = [];
    
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
    
    def explicitDependencies(self):
        explicit_dep_list = [];
        library_refs = set(map(lambda ref: ref.fileRef, self.linkedLibraries()));
        dependency_refs = set(map(lambda dep: dep.target.productReference, self.dependencies));
        explicit_dep_list.extend(library_refs.intersection(dependency_refs));
        return explicit_dep_list;
    
    def implicitDependencies(self):
        implicit_dep_list = [];
        library_refs = set(map(lambda ref: ref.fileRef, self.linkedLibraries()));
        dependency_refs = set(map(lambda dep: dep.target.productReference, self.dependencies));
        implicit_dep_list.extend(library_refs.difference(dependency_refs));
        return implicit_dep_list;