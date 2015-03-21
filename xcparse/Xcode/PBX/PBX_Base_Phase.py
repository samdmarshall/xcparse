from .PBXResolver import *
from .PBX_Base import *
from .PBX_Constants import *

class PBX_Base_Phase(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBX_Base_Phase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = '';
        self.phase_type = 'BASE';
        
        if kPBX_PHASE_buildActionMask in dictionary.keys():
            self.buildActionMask = dictionary[kPBX_PHASE_buildActionMask];
        
        self.files = [];
        if kPBX_PHASE_files in dictionary.keys():
            self.files = self.parseProperty(kPBX_PHASE_files, lookup_func, dictionary, project, True);
        
        if kPBX_PHASE_runOnlyForDeploymentPostprocessing in dictionary.keys():
            self.runOnlyForDeploymentPostprocessing = dictionary[kPBX_PHASE_runOnlyForDeploymentPostprocessing];
        
    def performPhase(self, build_system, target):
        phase_spec = build_system.getSpecForIdentifier(self.bundleid);
        print '%s Phase: %s' % (self.phase_type, phase_spec.name);
        print '* %s' % (phase_spec.contents['Description']);
        print '(implement me!)';
        print '';