from .PBXResolver import *
from .PBX_Base import *
from .PBX_Constants import *

class PBXBuildFile(PBX_Base):
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXBuildFile, self).__init__(lookup_func, dictionary, project, identifier);
        if kPBX_BUILDFILE_fileRef in dictionary.keys():
            self.fileRef = self.parseProperty(kPBX_BUILDFILE_fileRef, lookup_func, dictionary, project, False);
            self.name = self.fileRef.name;
        if kPBX_BUILDFILE_settings in dictionary.keys():
            self.settings = dictionary[kPBX_BUILDFILE_settings];