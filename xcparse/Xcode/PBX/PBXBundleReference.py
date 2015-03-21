import os
from ...Helpers import path_helper
from .PBX_Base_Reference import *

class PBXBundleReference(PBX_Base_Reference):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXBundleReference, self).__init__(lookup_func, dictionary, project, identifier);
        self.path = None;
        self.fs_path = None;
        if 'path' in dictionary.keys():
            self.path = path_helper(dictionary['path'], '');
            self.name = os.path.basename(self.path.obj_path);
        if 'refType' in dictionary.keys():
            self.refType = dictionary['refType'];
        if 'sourceTree' in dictionary.keys():
            self.sourceTree = dictionary['sourceTree'];