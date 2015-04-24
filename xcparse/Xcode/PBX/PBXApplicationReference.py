from .PBX_Base_Reference import *
from ...Helpers import path_helper

class PBXApplicationReference(PBX_Base_Reference):
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXApplicationReference, self).__init__(lookup_func, dictionary, project, identifier);