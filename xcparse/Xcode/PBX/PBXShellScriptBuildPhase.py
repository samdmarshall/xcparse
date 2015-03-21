from .PBXResolver import *
from .PBX_Base_Phase import *
from .PBX_Constants import *

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
        if kPBX_PHASE_showEnvVarsInLog in dictionary.keys():
            self.showEnvVarsInLog = dictionary[kPBX_PHASE_showEnvVarsInLog];