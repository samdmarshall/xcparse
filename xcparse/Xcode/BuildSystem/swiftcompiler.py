import os
from .xccompiler import *
from ...Helpers import logging_helper
from ...Helpers import xcrun_helper

class swiftcompiler(xccompiler):
    
    def __init__(self, compiler, config_dict):
        super(swiftcompiler, self).__init__(compiler, config_dict);
        
    def build(self):
        build_system = self.properties['buildsystem'];
        arch = self.properties['arch'];
        
        args = ();
        # add base (compiler)
        args += self.properties['baseargs'];
        
        # I think this should be handled by something in the xcspec
        sdk_name = build_system.environment.valueForKey('SDKROOT');
        sdk_path = xcrun_helper.make_xcrun_with_args(('--sdk', sdk_name, '--show-sdk-path'));
        args += ('-sdk', sdk_path);
        
        # this is missing all the build settings, also needs output set
        resolved_values = build_system.environment.resolvedValues();
        environment_variables_has_flags = filter(lambda envar: hasattr(envar, 'CommandLineArgs'), resolved_values.values());
        for envar in environment_variables_has_flags:
            result = envar.commandLineFlag(build_system.environment, resolved_values);
            if result != None and len(result) > 0:
                args += (result,);
        
        args += ('-c', );
        
        for file in self.properties['files']:
            file_path = str(file.fileRef.fs_path.root_path);
            args += (file_path, );
        
        # add -target
        deployment_target = '';
        platform = build_system.environment.valueForKey('PLATFORM_NAME');
        if platform == 'macosx':
            deployment_target = build_system.environment.valueForKey('MACOSX_DEPLOYMENT_TARGET');
        if platform == 'iphoneos':
            deployment_target = build_system.environment.valueForKey('IPHONEOS_DEPLOYMENT_TARGET');
            if deployment_target > '7.0':
                logging_helper.getLogger().error('[xcbuildsystem]: Cannot deploy swift to targets less than iOS 7.0');
        target_arch_platform_os = arch+'-apple-'+platform+deployment_target;
        args += ('-target', target_arch_platform_os);
        # add standard flags
        module_cache_path = os.path.join(xcrun_helper.ResolveDerivedDataPath(), 'ModuleCache')
        args += ('-module-cache-path', module_cache_path);
        source_root = build_system.environment.valueForKey('SRCROOT');
        config_build_dir = build_system.environment.valueForKey('CONFIGURATION_BUILD_DIR');
        args += ('-I', os.path.join(source_root, config_build_dir));
        args += ('-F', os.path.join(source_root, config_build_dir));
        args += ('-parseable-output', );
        args += ('-serialize-diagnostics', );
        args += ('-emit-dependencies', );
        args += ('-emit-module', );
        module_path = '';
        args += ('-emit-module-path', module_path);
        # add diag
        args += ('',);
                    
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