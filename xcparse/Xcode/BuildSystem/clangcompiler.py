import os
from .xccompiler import *
from ...Helpers import logging_helper
from ...Helpers import xcrun_helper

class clangcompiler(xccompiler):
    
    def __init__(self, compiler, config_dict):
        super(clangcompiler, self).__init__(compiler, config_dict);
    
    def build(self):
        build_system = self.properties['buildsystem'];
        arch = self.properties['arch'];
        
        for file in self.properties['files']:
            
            args = ();
            # add base (compiler)
            args += self.properties['baseargs'];
            
            sdk_name = build_system.environment.valueForKey('SDKROOT');
            sdk_path = xcrun_helper.make_xcrun_with_args(('--sdk', sdk_name, '--show-sdk-path'));
            
            # add language dialect
            found_dialect = False;
            identifier = file.fileRef.ftype;
            language = '';
            while found_dialect == False:
                file_ref_spec = build_system.getSpecForIdentifier(identifier);
                if file_ref_spec != None:
                    if 'GccDialectName' not in file_ref_spec.contents.keys():
                        identifier = file_ref_spec.basedOn.identifier;
                    else:
                        language = file_ref_spec.contents['GccDialectName'];
                        found_dialect = True;
                else:
                    break;
            
            if found_dialect == True:
                args += ('-x', language);
            
            args += ('-isysroot', sdk_path);
            
            # this is missing all the build settings, also needs output set
            environment_variables_has_flags = filter(lambda envar: hasattr(envar, 'CommandLineArgs'), build_system.environment.resolvedValues().values());
            for envar in environment_variables_has_flags:
                result = envar.commandLineFlag(build_system.environment);
                if result != None and len(result) > 0:
                    args += (result,);
            
            file_path = str(file.fileRef.fs_path.root_path);
            args += ('-c', file_path);
            
            # add arch
            args += ('-arch', self.properties['arch']);
            # add diag
            args += ('',);
            # add output
            args += ('-o', '<some output file path>')
            
            # this is displaying the command being issued for this compiler in the build phase
            args_str = '';
            for word in args:
                args_str += word;
                args_str += ' ';
            print '\t'+args_str;
            
            # this is running the compiler command
            # compiler_output = xcrun_helper.make_subprocess_call(args);
            # if compiler_output[1] != 0:
            #     logging_helper.getLogger().error('[xcbuildsystem]: Compiler error %s' % compiler_output[0]);