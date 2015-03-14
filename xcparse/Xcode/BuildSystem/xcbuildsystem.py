from __future__ import absolute_import
import os
import sys
import importlib

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
        found_specs = self.__findFilesFromPath('../Plugins', 'xcspec');
        
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
        
        self.environment = Environment();
    
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
        print compiler;
        
        return compiler;
        