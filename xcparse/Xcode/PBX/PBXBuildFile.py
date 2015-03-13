from .PBXResolver import *
from .PBX_Base import *

class PBXBuildFile(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        self.name = '';
        if 'fileRef' in dictionary.keys():
            self.fileRef = self.parseProperty('fileRef', lookup_func, dictionary, project, False);
            self.name = self.fileRef.name;
        if 'settings' in dictionary.keys():
            self.settings = dictionary['settings'];