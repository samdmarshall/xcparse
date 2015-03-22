from .PBXResolver import *
from .PBX_Base_Phase import *
from ...Helpers import logging_helper
from ...Helpers import xcrun_helper
from ..BuildSystem.Environment import Environment

class PBXSourcesBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXSourcesBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.sources';
        self.phase_type = 'Compile Sources';
    
    def performPhase(self, build_system, target):
        phase_spec = build_system.getSpecForIdentifier(self.bundleid);
        print '%s Phase: %s' % (self.phase_type, phase_spec.name);
        print '* %s' % (phase_spec.contents['Description']);
        
        compiler_dict = {};
        
        # this groups files based on compiler
        for file in self.files:
            file_spec = build_system.getSpecForIdentifier(file.fileRef.ftype);
            compiler = build_system.getCompilerForFileReference(file.fileRef);
            logging_helper.getLogger().info('[PBXSourcesBuildPhase]: File "%s" wants Compiler "%s"' % (file, compiler));
            
            if compiler.identifier not in compiler_dict.keys():
                compiler_dict[compiler.identifier] = set();
            if compiler.identifier in compiler_dict.keys():
                compiler_dict[compiler.identifier].add(file);
        
        # this iterates over the grouped (compiler:files) key:value pairs to create the build objects for those files
        for compiler_key in compiler_dict.keys():
            build_system.compiler = build_system.getSpecForIdentifier(compiler_key);
            files = compiler_dict[compiler_key];
            build_system.compileFiles(files);
        
        print '';