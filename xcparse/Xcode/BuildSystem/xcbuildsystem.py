from __future__ import absolute_import
import os
import sys
import importlib
from ...Helpers import logging_helper
from ...Helpers import plist_helper
from ...Helpers import xcrun_helper
from .xcspec_helper import *
from .xcbuildrule import *
from .LangSpec.langspec import *
from .xcplatform import *
from .Environment import Environment

class xcbuildsystem(object):
    
    def __init__(self):
        self.specs = set();
        # loading default specs
        found_specs = self.__findFilesFromPath('../Plugins', 'spec');
        
        for path in found_specs:
            self.specs.update(xcspecLoadFromContentsAtPath(path));
        
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
    
    def initEnvironment(self, project, configuration_name):
        if self.environment == None:
            self.environment = Environment();
        else:
            logging_helper.getLogger().warn('[xcbuildsystem]: Already initialized environment!');
        self.environment.setValueForKey('CONFIGURATION', configuration_name, {});
        self.environment.setValueForKey('ACTION', 'build', {});
        self.environment.setValueForKey('SRCROOT', project.path.base_path, {});
        self.environment.setValueForKey('PROJECT_DIR', project.path.base_path, {});
        self.environment.setValueForKey('PROJECT_NAME', project.rootObject.name.split('.')[0], {});
        self.environment.setValueForKey('CONFIGURATION_BUILD_DIR', '$(SYMROOT)/$(CONFIGURATION)', {});
    
    def __findFilesFromPath(self, path, extension):
        found_items = [];
        search_path = os.path.normpath(os.path.join(xcrun_helper.resolve_developer_path(), path));
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
    
    def getCompilerForFileReference(self, file_ref):
        file_ref_spec = self.getSpecForIdentifier(file_ref.ftype);
        file_types = file_ref_spec.inheritedTypes();
        
        # this calculates the best guess compiler from the input file types
        compiler_identifier = '';
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
    
    def compileFiles(self, files):
        
        if self.compiler != None:
            args = ();
            
            # setting up default build environments
            if 'Options' in self.compiler.contents.keys():
                self.environment.addOptions(self.compiler.contents['Options']);
        
            compiler_exec = '';
            if 'ExecPath' in self.compiler.contents.keys():
                if self.environment.isEnvironmentVariable(self.compiler.contents['ExecPath']) == True:
                    compiler_exec_results = self.environment.parseKey(self.compiler.contents['ExecPath']);
                    if compiler_exec_results[0] == True:
                        compiler_exec = xcrun_helper.make_xcrun_with_args(('-f', str(compiler_exec_results[1])));
            else:
                logging_helper.getLogger().error('[xcbuildsystem]: No compiler executable found!');
                return;
            
            args += (compiler_exec,);
            
            for file in files:
                file_path = str(file.fileRef.fs_path.root_path);
                args += (file_path,)
            
            sdk_name = self.environment.valueForKey('SDKROOT');
            sdk_path = xcrun_helper.make_xcrun_with_args(('--sdk', sdk_name, '--show-sdk-path'));
            if self.compiler.identifier == 'com.apple.xcode.tools.swift.compiler':
                args += ('-sdk', sdk_path);
            elif self.compiler.identifier.startswith('com.apple.xcode.compiler.llvm.clang'):
                args += ('-isysroot', sdk_path);
            else:
                logging_helper.getLogger().warn('[xcbuildsystem]: unknown compiler, not sure how to specify sdk path');
            
            # this is missing all the build settings, also needs output set
            
            # this is displaying the command being issued for this compiler in the build phase
            args_str = '';
            for word in args:
                args_str += word;
                args_str += ' ';
            print args_str;
            
            # this is running the compiler command
            compiler_output = xcrun_helper.make_subprocess_call(args);
            if compiler_output[1] != 0:
                logging_helper.getLogger().error('[xcbuildsystem]: Compiler error %s' % compiler_output[0]);
        else:
            logging_helper.getLogger().error('[xcbuildsystem]: No compiler set!');