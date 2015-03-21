from .PBXResolver import *
from .PBX_Base import *

class PBXTargetDependency(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXTargetDependency, self).__init__(lookup_func, dictionary, project, identifier);
        if 'target' in dictionary.keys():
            self.target = self.parseProperty('target', lookup_func, dictionary, project, False);
        if 'targetProxy' in dictionary.keys():
            self.proxy = self.parseProperty('targetProxy', lookup_func, dictionary, project, False);