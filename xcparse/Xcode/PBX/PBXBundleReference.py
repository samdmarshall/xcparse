import os
from ...Helpers import path_helper
from .PBX_Base_Reference import *

class PBXBundleReference(PBX_Base_Reference):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXBundleReference, self).__init__(lookup_func, dictionary, project, identifier);
        