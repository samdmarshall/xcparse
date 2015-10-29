import os
from .xccompiler import *
from ...Helpers import logging_helper
from ...Helpers import xcrun_helper
from ...Helpers import path_helper

class clangcompiler(xccompiler):
    
    def __init__(self, compiler, config_dict):
        super(clangcompiler, self).__init__(compiler, config_dict);
    
    def build(self):
        build_system = self.properties['buildsystem'];
        arch = self.properties['arch'];
        
        product_name = build_system.environment.parseKey(None, '$(PRODUCT_NAME)')[1];
        output_dir = build_system.environment.parseKey(None, '$(OBJECT_FILE_DIR_$(CURRENT_VARIANT))/$(CURRENT_ARCH)')[1];
        path_helper.create_directories(output_dir)
        link_file_list = os.path.join(output_dir, product_name+'.LinkFileList')
        link_file_list_fd = open(link_file_list, 'w');
        
        for file in self.properties['files']:
            
            file_name = file.name.split('.')[0];
            
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
            else:
                # should this be an error?
                logging_helper.getLogger().warn('[clangcompiler]: unknown language used: "%s"' % (language));
            # I think this should be handled by something in the xcspec
            args += ('-isysroot', sdk_path);
            
            # this is missing all the build settings, also needs output set
            resolved_settings = build_system.environment.resolvedValues();
            environment_variables_has_flags = filter(lambda envar: envar.hasCommandLineArgs() == True, resolved_settings.values());
            for envar in environment_variables_has_flags:
                if envar.satisfiesCondition(build_system.environment, resolved_settings) == True:
                    if hasattr(envar, 'FileTypes'):
                        file_ref_spec = build_system.getSpecForIdentifier(file.fileRef.ftype);
                        file_types = file_ref_spec.inheritedTypes();
                        skip_file = True;
                        for allowed_file_type_for_var in envar.FileTypes:
                            if allowed_file_type_for_var in file_types:
                                skip_file = False;
                                break;
                        if skip_file == True:
                            continue;
                    result = envar.commandLineFlag(build_system.environment, lookup_dict=resolved_settings);
                    if result != None and len(result) > 0:
                        args += (result,);
            
            file_path = str(file.fileRef.fs_path.root_path);
            args += ('-c', file_path);
            
            # # add arch
            # args += ('-arch', self.properties['arch']);
            # add diag
            args += ('',);
            # add output
            object_file = file_name + '.o';
            output_file_path = os.path.join(output_dir, object_file);
            # writing the object file path to the linkfilelist
            print >> link_file_list_fd, output_file_path;
            args += ('-o', output_file_path)
            
            # this is displaying the command being issued for this compiler in the build phase
            args_str = '';
            for word in args:
                flag = str(word)
                if flag != '\'\'':
                    args_str += flag
                    args_str += ' ';
            print '\t'+args_str;
            
            print '';
            # this is running the compiler command
            # compiler_output = xcrun_helper.make_subprocess_call(args);
            # if compiler_output[1] != 0:
            #     logging_helper.getLogger().error('[xcbuildsystem]: Compiler error %s' % compiler_output[0]);
        
        link_file_list_fd.close();