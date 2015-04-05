from __future__ import absolute_import
import os
import sys
import importlib
import grp
from ...Helpers import logging_helper
from ...Helpers import plist_helper
from ...Helpers import xcrun_helper
from .xccompiler import *
from .swiftcompiler import *
from .clangcompiler import *
from .xclinker import *
from .xcspec_helper import *
from .xcbuildrule import *
from .LangSpec.langspec import *
from .xcplatform import *
from .Environment import Environment

class xcbuildsystem(object):
    
    def __init__(self):
        self.specs = set();
        # loading default specs
        search_path = os.path.normpath(os.path.join(xcrun_helper.resolve_developer_path(), '../Plugins'));
        self.loadSpecsAtPath(search_path);
       
        
        # updating specs to point to each other and form inheritence.
        for spec_item in self.specs:
            if spec_item.basedOn != None:
                spec_item.basedOn = self.getSpecForIdentifier(spec_item.basedOn);
        
        self.languages = set();
        # loading default languages
        found_languages = self.__findFilesFromPath('../SharedFrameworks/DVTFoundation.framework/Versions/A/Resources', 'xclangspec');
        
        self.platforms = LoadPlatforms();
        
        # this should load until we know the environment needed
        self.environment = None;
        
        # this will be used for the current compiler
        self.compiler = None;
        
        # this will be used for the current linker
        self.linker = None;
    
    def loadSpecsAtPath(self, search_path):
        found_specs = self.__findFilesFromPath(search_path, 'spec');
        
        for path in found_specs:
            self.specs.update(xcspecLoadFromContentsAtPath(path));
    
    def initEnvironment(self, project, configuration_name):
        if self.environment == None:
            self.environment = Environment();
        else:
            logging_helper.getLogger().warn('[xcbuildsystem]: Already initialized environment!');
        self.environment.setValueForKey('BUILD_VARIANTS', 'normal', {});
        self.environment.setValueForKey('CONFIGURATION', configuration_name, {});
        self.environment.setValueForKey('SRCROOT', project.path.base_path, {});
        self.environment.setValueForKey('SOURCE_ROOT', '$(SRCROOT)', {});
        self.environment.setValueForKey('PROJECT_DIR', project.path.base_path, {});
        self.environment.setValueForKey('PROJECT_FILE_PATH', project.path.obj_path, {});
        self.environment.setValueForKey('PROJECT_NAME', project.rootObject.name.split('.')[0], {});
        self.environment.setValueForKey('PROJECT', project.rootObject.name.split('.')[0], {});
        self.environment.setValueForKey('USER', os.getlogin(), {});
        self.environment.setValueForKey('UID', str(os.geteuid()), {});
        self.environment.setValueForKey('GID', str(os.getegid()), {});
        self.environment.setValueForKey('GROUP', str(grp.getgrgid(os.getegid()).gr_name), {});
        self.environment.setValueForKey('USER_APPS_DIR', os.path.join(os.getenv('HOME'), 'Applications'), {});
        self.environment.setValueForKey('USER_LIBRARY_DIR', os.path.join(os.getenv('HOME'), 'Library'), {});
        self.environment.setValueForKey('DT_TOOLCHAIN_DIR', os.path.join(xcrun_helper.resolve_developer_path(), 'Toolchains/XcodeDefault.xctoolchain'), {});
    
    def __findFilesFromPath(self, search_path, extension):
        found_items = [];
        if os.path.exists(search_path) == True:
            for root, dirs, files in os.walk(search_path, followlinks=False):
                for name in files:
                    original_path = os.path.join(root, name);
                    if name.endswith(extension) == True:
                        found_items.append(original_path);
        return found_items;
    
    def getSpecForType(self, type):
        """
        Returns a list of specs with matching type string
        """
        return self.getSpecForFilter(lambda spec: spec.type == type);
    
    def getSpecForIdentifier(self, identifier):
        results = self.getSpecForFilter(lambda spec: spec.identifier == identifier);
        if results != None:
            return results[0];
        return results;
    
    def getSpecForFilter(self, filter_func):
        results = filter(filter_func, self.specs);
        if len(results) > 0:
            return results;
        else:
            return None;
    
    def buildRules(self):
        contents = [];
        
        # add the custom build rules from target here
        
        compilers = self.getSpecForFilter(lambda spec: spec.type == 'Compiler' or spec.identifier.startswith('com.apple.compiler'));
        for compiler in filter(lambda compiler: compiler.abstract == 'NO' or 'SynthesizeBuildRule' in compiler.contents.keys(), compilers):
            if 'SynthesizeBuildRule' in compiler.contents.keys():
                if compiler.contents['SynthesizeBuildRule'] == 'YES' or compiler.contents['SynthesizeBuildRule'] == 'Yes':
                    rule_dict = {};
                    rule_dict['CompilerSpec'] = compiler.identifier;
                    if 'FileTypes' in compiler.contents.keys():
                        rule_dict['FileType'] = compiler.contents['FileTypes'];
                    if 'InputFileTypes' in compiler.contents.keys():
                        rule_dict['FileType'] = compiler.contents['InputFileTypes'];
                    rule_dict['Name'] = compiler.name;
                    # do not add if there is no input to this rule
                    if 'FileType' in rule_dict.keys():
                        contents.append(xcbuildrule(rule_dict));
        
        build_rules_plist_path = os.path.normpath(os.path.join(xcrun_helper.resolve_developer_path(), '../Plugins/Xcode3Core.ideplugin/Contents/Frameworks/DevToolsCore.framework/Versions/A/Resources/BuiltInBuildRules.plist'));
        build_rules = plist_helper.LoadPlistFromDataAtPath(build_rules_plist_path);
        
        for rule in build_rules:
            contents.append(xcbuildrule(rule));
        return contents;
    
    def getCompilerForFileReference(self, file_ref, default_compiler_identifier):
        file_ref_spec = self.getSpecForIdentifier(file_ref.ftype);
        file_types = file_ref_spec.inheritedTypes();
        
        compiler_identifier = '';
        if default_compiler_identifier != None:
            default_compiler = self.getSpecForIdentifier(default_compiler_identifier);
            if default_compiler != None:
                if 'FileTypes' in default_compiler.contents.keys():
                    compiler_types_set = set(map(lambda ftype: str(ftype), default_compiler.contents['FileTypes']));
                    file_types_set = set(file_types);
                    result_set = file_types_set.intersection(compiler_types_set);
                    if len(result_set) > 0:
                        compiler_identifier = default_compiler_identifier;
        # this calculates the best guess compiler from the input file types
        if compiler_identifier == '':
            compiler_weight = 100;
            for rule in self.buildRules():
                rule_weight = 0;
                for ftype in file_types:
                    if ftype in rule.fileTypes:
                        break;
                    rule_weight += 1;
                if compiler_weight > rule_weight:
                    compiler_weight = rule_weight;
                    compiler_identifier = rule.identifier;
        compiler = self.getSpecForIdentifier(compiler_identifier);
        if compiler == None:
            logging_helper.getLogger().info('[xcbuildsystem]: Could not find valid build rule for input file!');
        return compiler;
    
    def processFiles(self, files, function):
        # getting the build variant
        compile_variants = [];
        variant_value = self.environment.valueForKey('BUILD_VARIANTS');
        compile_variants.extend(variant_value.split(' '));
        for variant in compile_variants:
            self.environment.setValueForKey('CURRENT_VARIANT', variant, {});
            self.environment.setValueForKey('variant', variant, {});
            self.environment.setValueForKey('OBJECT_FILE_DIR', '$(TARGET_TEMP_DIR)/Objects', {});
            self.environment.setValueForKey('OBJECT_FILE_DIR_'+variant, '$(OBJECT_FILE_DIR)-$(CURRENT_VARIANT)', {});
            # getting the architectures
            compile_archs = [];
            resolved_values = self.environment.resolvedValues();
            arch_value = resolved_values['ARCHS'].value(self.environment, lookup_dict=resolved_values);
            compile_archs.extend(arch_value.split(' '));
            for arch in compile_archs:
                # iterate the architectures
                self.environment.setValueForKey('CURRENT_ARCH', arch, {});
                self.environment.setValueForKey('arch', arch, {});
                
                if callable(function):
                    function(files);
                
                # newline between each architecture
                print '';
            # newline between each variant
            print '';
    
    def compileFiles(self, files):
        if self.compiler != None:
            base_args = ();
            
            # setting up default build environments
            if 'Options' in self.compiler.contents.keys():
                self.environment.addOptions(self.compiler.contents['Options']);
            
            compiler_exec = '';
            if 'ExecPath' in self.compiler.contents.keys():
                compiler_path = self.compiler.contents['ExecPath'];
                if self.environment.isEnvironmentVariable(compiler_path) == True:
                    compiler_exec_results = self.environment.parseKey(None, self.compiler.contents['ExecPath']);
                    if compiler_exec_results[0] == True:
                        compiler_path = str(compiler_exec_results[1]);
                compiler_exec = xcrun_helper.make_xcrun_with_args(('-f', compiler_path));
            else:
                logging_helper.getLogger().error('[xcbuildsystem]: No compiler executable found!');
                return;
            
            base_args += (compiler_exec,);
            
            config_dict = {
                'variant': self.environment.valueForKey('variant'),
                'arch': self.environment.valueForKey('arch'),
                'files': files,
                'environment': self.environment,
                'buildsystem': self,
                'baseargs': base_args,
            };
            
            compiler_instance = None;
            if self.compiler.identifier == 'com.apple.xcode.tools.swift.compiler':
                compiler_instance = swiftcompiler(self.compiler, config_dict);
            elif self.compiler.identifier.startswith('com.apple.compilers.llvm.clang'):
                compiler_instance = clangcompiler(self.compiler, config_dict);
            else:
                logging_helper.getLogger().error('[xcbuildsystem]: unknown compiler %s' % self.compiler);
            
            if compiler_instance != None:
                compiler_instance.build();
            
            if 'Options' in self.compiler.contents.keys():
                self.environment.removeOptions(self.compiler.contents['Options']);
                
        else:
            logging_helper.getLogger().error('[xcbuildsystem]: No compiler set!');
    
    def linkFiles(self, files):
        if self.linker != None:
            base_args = ();
            
            # setting up default build environments
            if 'Options' in self.linker.contents.keys():
                self.environment.addOptions(self.linker.contents['Options']);
            
            linker_exec = '';
            if 'Name' in self.linker.contents.keys():
                linker_path = self.linker.contents['Name'];
                linker_exec = xcrun_helper.make_xcrun_with_args(('-f', linker_path));
            else:
                logging_helper.getLogger().error('[xcbuildsystem]: No linker executable found!');
                return;
            
            base_args += (linker_exec,);
            
            product_name = self.environment.parseKey(None, '$(PRODUCT_NAME)')[1];
            output_dir = self.environment.parseKey(None, '$(OBJECT_FILE_DIR_$(CURRENT_VARIANT))/$(CURRENT_ARCH)')[1];
        
            link_file_list = os.path.join(output_dir, product_name+'.LinkFileList')
        
            link_file_input_var = self.environment.parseKey(None, 'LINK_FILE_LIST_$(variant)_$(arch)')[1]
            self.environment.setValueForKey(str(link_file_input_var), link_file_list, {});
            
            config_dict = {
                'variant': self.environment.valueForKey('variant'),
                'arch': self.environment.valueForKey('arch'),
                'files': files,
                'environment': self.environment,
                'buildsystem': self,
                'baseargs': base_args,
            };
            
            linker_instance = xclinker(self.linker, config_dict);
            
            if linker_instance != None:
                linker_instance.link();
            
            if 'Options' in self.linker.contents.keys():
                self.environment.removeOptions(self.linker.contents['Options']);
        else:
            logging_helper.getLogger().error('[xcbuildsystem]: No linker set!');
        