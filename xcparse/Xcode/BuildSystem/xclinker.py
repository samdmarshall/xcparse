import os
from ...Helpers import logging_helper
from ...Helpers import xcrun_helper

class xclinker(object):
    
    def __init__(self, linker, config_dict):
        self.linker = linker;
        self.properties = config_dict;
    
    def link(self):
        build_system = self.properties['buildsystem'];
        arch = self.properties['arch'];
        
        args = ();
        # add base (compiler)
        args += self.properties['baseargs'];
        
        # add arch
        args += ('-arch', self.properties['arch']);
        
        sdk_name = build_system.environment.valueForKey('SDKROOT');
        sdk_path = xcrun_helper.make_xcrun_with_args(('--sdk', sdk_name, '--show-sdk-path'));
        args += ('-isysroot', sdk_path);
        
        resolved_settings = build_system.environment.resolvedValues();
        environment_variables_has_flags = filter(lambda envar: envar.hasCommandLineArgs() == True, resolved_settings.values());
        for envar in environment_variables_has_flags:
            if envar.satisfiesCondition(build_system.environment, resolved_settings) == True:
                result = envar.commandLineFlag(build_system.environment, lookup_dict=resolved_settings);
                if result != None and len(result) > 0:
                    args += (result,);
        
        args_str = '';
        for word in args:
            args_str += word;
            args_str += ' ';
        print '\t'+args_str;