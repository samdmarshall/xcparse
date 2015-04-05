from .PBXResolver import *
from .PBXSourcesBuildPhase import *
from .PBXFrameworksBuildPhase import *
from .PBX_Build_Setting import *
from .PBX_Constants import *

class PBX_Base_Target(PBX_Build_Setting):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBX_Base_Target, self).__init__(lookup_func, dictionary, project, identifier);
        self.project_container = project;
        
        if kPBX_TARGET_name in dictionary.keys():
            self.name = dictionary[kPBX_TARGET_name];
        
        self.productName = '';
        if kPBX_TARGET_productName in dictionary.keys():
            self.productName = dictionary[kPBX_TARGET_productName];
        
        if kPBX_TARGET_buildConfigurationList in dictionary.keys():
            self.buildConfigurationList = self.parseProperty(kPBX_TARGET_buildConfigurationList, lookup_func, dictionary, project, False);
        
        self.buildPhases = [];
        if kPBX_TARGET_buildPhases in dictionary.keys():
            self.buildPhases = self.parseProperty(kPBX_TARGET_buildPhases, lookup_func, dictionary, project, True);
        
        self.dependencies = [];
        if kPBX_TARGET_dependencies in dictionary.keys():
            self.dependencies = self.parseProperty(kPBX_TARGET_dependencies, lookup_func, dictionary, project, True);
        
        if kPBX_TARGET_productReference in dictionary.keys():
            self.productReference = self.parseProperty(kPBX_TARGET_productReference, lookup_func, dictionary, project, False);
        
        if kPBX_TARGET_productType in dictionary.keys():
            self.productType = dictionary[kPBX_TARGET_productType];
    
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
    
    def executeBuildPhases(self, build_system):
        for phase in self.buildPhases:
            phase.performPhase(build_system, self);