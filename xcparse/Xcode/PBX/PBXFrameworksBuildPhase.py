from .PBX_Base_Phase import *

class PBXFrameworksBuildPhase(PBX_Base_Phase):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXFrameworksBuildPhase, self).__init__(lookup_func, dictionary, project, identifier);
        self.bundleid = 'com.apple.buildphase.frameworks';
        self.phase_type = 'Link Libraries';
    
    
    def performPhase(self, build_system, target):
        phase_spec = build_system.getSpecForIdentifier(self.bundleid);
        print '%s Phase: %s' % (self.phase_type, phase_spec.name);
        print '* %s' % (phase_spec.contents['Description']);
        
        # as far as I can tell, the linker is chosen based on binary type. There doesn't seem to be rules in place for handling it per platform 
        # as a result this is just going to be hardcoded to check for static lib target type to use libtool otherwise use ld
        linker_identifier = '';
        product_type = build_system.environment.valueForKey('MACH_O_TYPE');
        if product_type == 'staticlib':
            linker_identifier = 'com.apple.pbx.linkers.libtool';
        else:
            linker_identifier = 'com.apple.pbx.linkers.ld';
        
        build_system.linker = build_system.getSpecForIdentifier(linker_identifier);
        
        # send files off to the linker
        build_system.processFiles(self.files, build_system.linkFiles);
        
        print '';