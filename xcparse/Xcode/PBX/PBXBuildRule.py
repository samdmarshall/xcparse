from .PBXResolver import *
from .PBX_Base import *

class PBXBuildRule(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXBuildRule, self).__init__(lookup_func, dictionary, project, identifier);
        if 'compilerSpec' in dictionary.keys():
            self.compilerSpec = dictionary['compilerSpec'];
        if 'filePatterns' in dictionary.keys():
            self.filePatterns = dictionary['filePatterns'];
        if 'fileType' in dictionary.keys():
            self.fileType = dictionary['fileType'];
        if 'isEditable' in dictionary.keys():
            self.isEditable = dictionary['isEditable'];
        if 'outputFiles' in dictionary.keys():
            self.outputFiles = dictionary['outputFiles'];
        if 'script' in dictionary.keys():
            self.script = dictionary['script'];