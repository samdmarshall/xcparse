import os
from .PBX_Base_Reference import *
from ...Helpers import path_helper

class PBXFrameworkReference(PBX_Base_Reference):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXFrameworkReference, self).__init__(lookup_func, dictionary, project, identifier);
        