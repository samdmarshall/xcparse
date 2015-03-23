from .PBXResolver import *
from .PBX_Base_Phase import *
from .PBX_Constants import *
from ...Helpers import logging_helper
from ...Helpers import xcrun_helper
from ...Helpers import path_helper

class PBXShellScriptBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXShellScriptBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.shell-script';
        self.phase_type = 'Run Shell Script';
        if kPBX_PHASE_shellScript in dictionary.keys():
            self.shellScript = dictionary[kPBX_PHASE_shellScript];
        if kPBX_PHASE_shellPath in dictionary.keys():
            self.shellPath = dictionary[kPBX_PHASE_shellPath];
        if kPBX_PHASE_inputPaths in dictionary.keys():
            inputPaths = [];
            for inputPath in dictionary[kPBX_PHASE_inputPaths]:
                inputPaths.append(inputPath);
            self.inputPaths = inputPaths;
        if kPBX_PHASE_outputPaths in dictionary.keys():
            outputPaths = [];
            for outputPath in dictionary[kPBX_PHASE_outputPaths]:
                outputPaths.append(outputPath);
            self.outputPaths = outputPaths;
        self.showEnvVarsInLog = 1;
        if kPBX_PHASE_showEnvVarsInLog in dictionary.keys():
            self.showEnvVarsInLog = dictionary[kPBX_PHASE_showEnvVarsInLog];
    
    def performPhase(self, build_system, target):
        phase_spec = build_system.getSpecForIdentifier(self.bundleid);
        print '%s Phase: %s' % (self.phase_type, phase_spec.name);
        print '* %s' % (phase_spec.contents['Description']);
        
        config_name = build_system.environment.valueForKey('CONFIGURATION');
        symroot = build_system.environment.valueForKey('SYMROOT');
        # temp until this is resolved correctly
        symroot = 'build';
        
        script_dir_path = xcrun_helper.IntermediatesBuildLocation(target.project_container.rootObject, target.name, config_name, symroot);
        path_helper.create_directories(script_dir_path);
        script_path = os.path.join(script_dir_path, str('Script-'+self.identifier+'.sh'));
        
        fd = open(script_path, 'w');
        env = '#!' + self.shellPath
        print >> fd, env;
        print >> fd, self.shellScript;
        fd.close();
        
        if self.showEnvVarsInLog == 1:
            for key in sorted(build_system.environment.settings.keys()):
                # this need to change to parse out the resulting values completely
                print '\texport '+key+'='+build_system.environment.valueForKey(key);
        
        # this needs to export the environment variables
        print '/bin/sh -c '+script_path;
        # print xcrun_helper.make_subprocess_call(('/bin/sh','-c', script_path));
        
        print '';