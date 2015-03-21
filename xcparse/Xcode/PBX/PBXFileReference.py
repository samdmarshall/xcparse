import os
from .PBX_Base_Reference import *
from .PBX_Constants import *
from ...Helpers import path_helper

class PBXFileReference(PBX_Base_Reference):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXFileReference, self).__init__(lookup_func, dictionary, project, identifier);
        if kPBX_REFERENCE_lastKnownFileType in dictionary.keys():
            self.ftype = dictionary[kPBX_REFERENCE_lastKnownFileType];
        if kPBX_REFERENCE_fileEncoding in dictionary.keys():
            self.fileEncoding = dictionary[kPBX_REFERENCE_fileEncoding];
        if kPBX_REFERENCE_explicitFileType in dictionary.keys():
            self.explicitFileType = dictionary[kPBX_REFERENCE_explicitFileType];
        if kPBX_REFERENCE_includeInIndex in dictionary.keys():
            self.includeInIndex = dictionary[kPBX_REFERENCE_includeInIndex];