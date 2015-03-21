import os
from .PBX_Base_Reference import *
from ...Helpers import path_helper

class PBXLibraryReference(PBX_Base_Reference):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXLibraryReference, self).__init__(lookup_func, dictionary, project, identifier);
        self.path = None;
        self.fs_path = None;
        if 'path' in dictionary.keys():
            self.path = path_helper(dictionary['path'], '');
            self.name = os.path.basename(self.path.obj_path);
        if 'refType' in dictionary.keys():
            self.refType = dictionary['refType'];
        if 'sourceTree' in dictionary.keys():
            self.sourceTree = dictionary['sourceTree'];