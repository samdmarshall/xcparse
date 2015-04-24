from .PBXResolver import *
from .PBX_Base_Target import *

class PBXAggregateTarget(PBX_Base_Target):
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXAggregateTarget, self).__init__(lookup_func, dictionary, project, identifier);