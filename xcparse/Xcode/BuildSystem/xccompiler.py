import os
from ...Helpers import logging_helper
from ...Helpers import xcrun_helper

class xccompiler(object):
    
    def __init__(self, compiler, config_dict):
        self.compiler = compiler;
        self.properties = config_dict;
    
    def build(self):
        for file in self.properties['files']:
            
            args = ();
            # add base (compiler)
            args += self.properties['baseargs'];
            
            sdk_name = self.properties['environment'].valueForKey('SDKROOT');
            sdk_path = xcrun_helper.make_xcrun_with_args(('--sdk', sdk_name, '--show-sdk-path'));
            if self.compiler.identifier == 'com.apple.xcode.tools.swift.compiler':
                args += ('-sdk', sdk_path);
            elif self.compiler.identifier.startswith('com.apple.compilers.llvm.clang'):
                # add language dialect
                found_dialect = False;
                identifier = file.fileRef.ftype;
                language = '';
                while found_dialect == False:
                    file_ref_spec = self.properties['buildsystem'].getSpecForIdentifier(identifier);
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
            else:
                logging_helper.getLogger().warn('[xcbuildsystem]: unknown compiler, not sure how to specify sdk path');
            
            
            # this is missing all the build settings, also needs output set
            environment_variables_has_flags = filter(lambda envar: hasattr(envar, 'CommandLineArgs'), self.properties['environment'].settings.values());
            for envar in environment_variables_has_flags:
                result = envar.commandLineFlag(self.properties['environment']);
                if result != None and len(result) > 0:
                    args += (result,);
            
            file_path = str(file.fileRef.fs_path.root_path);
            args += ('-c', file_path);
            
            # add diags and compiler specific flags
            if self.compiler.identifier == 'com.apple.xcode.tools.swift.compiler':
                # add -target
                deployment_target = '';
                platform = self.properties['environment'].valueForKey('PLATFORM_NAME');
                if platform == 'macosx':
                    deployment_target = self.properties['environment'].valueForKey('MACOSX_DEPLOYMENT_TARGET');
                if platform == 'iphoneos':
                    deployment_target = self.properties['environment'].valueForKey('IPHONEOS_DEPLOYMENT_TARGET');
                    if deployment_target > '7.0':
                        logging_helper.getLogger().error('[xcbuildsystem]: Cannot deploy swift to targets less than iOS 7.0');
                target_arch_platform_os = self.properties['arch']+'-apple-'+platform+deployment_target;
                args += ('-target', target_arch_platform_os);
                # add standard flags
                module_cache_path = os.path.join(xcrun_helper.ResolveDerivedDataPath(), 'ModuleCache')
                args += ('-module-cache-path', module_cache_path);
                args += ('-I', os.path.join(self.properties['environment'].valueForKey('SRCROOT'), self.properties['environment'].valueForKey('CONFIGURATION_BUILD_DIR')));
                args += ('-F', os.path.join(self.properties['environment'].valueForKey('SRCROOT'), self.properties['environment'].valueForKey('CONFIGURATION_BUILD_DIR')));
                args += ('-parseable-output', );
                args += ('-serialize-diagnostics', );
                args += ('-emit-dependencies', );
                args += ('-emit-module', );
                module_path = '';
                args += ('-emit-module-path', module_path);
                # add diag
                args += ('',);
            elif self.compiler.identifier.startswith('com.apple.compilers.llvm.clang'):
                # add arch
                args += ('-arch', self.properties['arch']);
                # add diag
                args += ('',);
                # add output
                args += ('-o', '<some output file path>')
            else:
                logging_helper.getLogger().warn('[xcbuildsystem]: unable to determine compiler, not sure how to specify diags');
            
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