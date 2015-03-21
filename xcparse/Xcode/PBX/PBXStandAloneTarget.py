from .PBXResolver import *
from .PBX_Base_Target import *
from .PBX_Constants import *

class PBXStandAloneTarget(PBX_Base_Target):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXStandAloneTarget, self).__init__(lookup_func, dictionary, project, identifier);
        if kPBX_TARGET_buildRules in dictionary.keys():
            self.buildRules = self.parseProperty(kPBX_TARGET_buildRules, lookup_func, dictionary, project, True);
        if kPBX_TARGET_productType in dictionary.keys():
            self.productType = dictionary[kPBX_TARGET_productType];
        if kPBX_TARGET_buildProperties in dictionary.keys():
            self.buildProperties = dictionary[kPBX_TARGET_buildProperties];
            