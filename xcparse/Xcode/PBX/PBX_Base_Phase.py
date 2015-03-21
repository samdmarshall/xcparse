from .PBXResolver import *
from .PBX_Base import *

class PBX_Base_Phase(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBX_Base_Phase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = '';
        self.phase_type = 'BASE';
        self.files = [];
        
    def performPhase(self, build_system, target):
        phase_spec = build_system.getSpecForIdentifier(self.bundleid);
        print '%s Phase: %s' % (self.phase_type, phase_spec.name);
        print '* %s' % (phase_spec.contents['Description']);
        print '(implement me!)';
        print '';