from .PBXResolver import *
from .PBX_Base_Phase import *

class PBXShellScriptBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.bundleid = 'com.apple.buildphase.shell-script';
        self.identifier = identifier;
        self.phase_type = 'Run Shell Script';
        if 'buildActionMask' in dictionary.keys():
            self.buildActionMask = dictionary['buildActionMask'];
        if 'files' in dictionary.keys():
            self.files = self.parseProperty('files', lookup_func, dictionary, project, True);
        if 'runOnlyForDeploymentPostprocessing' in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary['runOnlyForDeploymentPostprocessing'];
        if 'shellScript' in dictionary.keys():
            self.shellScript = dictionary['shellScript'];
        if 'shellPath' in dictionary.keys():
            self.shellPath = dictionary['shellPath'];
        if 'inputPaths' in dictionary.keys():
            inputPaths = [];
            for inputPath in dictionary['inputPaths']:
                inputPaths.append(inputPath);
            self.inputPaths = inputPaths;
        if 'outputPaths' in dictionary.keys():
            outputPaths = [];
            for outputPath in dictionary['outputPaths']:
                outputPaths.append(outputPath);
            self.outputPaths = outputPaths;
        if 'showEnvVarsInLog' in dictionary.keys():
            self.showEnvVarsInLog = dictionary['showEnvVarsInLog'];