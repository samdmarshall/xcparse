from __future__ import absolute_import
import os
import sys
import importlib
import plistlib

from ..xcrun import *
from .xcspec_helper import *
from .xcbuildrule import *

class xcbuildsystem(object):
    
    def __init__(self):
        self.specs = set();
        # loading default specs
        found_specs = [];
        search_path = os.path.normpath(os.path.join(xcrun.resolve_developer_path(), '../Plugins'));
        if os.path.exists(search_path) == True:
            for root, dirs, files in os.walk(search_path, followlinks=False):
                for name in files:
                    original_path = os.path.join(root, name);
                    if name.endswith('xcspec') == True:
                        found_specs.append(original_path);
        
        for path in found_specs:
            self.specs.update(xcspecLoadFromContentsAtPath(path));
        
        # updating specs to point to each other and form inheritence.
        for spec_item in self.specs:
            if spec_item.basedOn != None:
                spec_item.basedOn = self.getSpecForIdentifier(spec_item.basedOn);
    
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
        # build_rules_plist_path = os.path.normpath(os.path.join(xcrun.resolve_developer_path(), '../OtherFrameworks/DevToolsCore.framework/Resources/Built-in build rules.plist'));
        # if os.path.exists(build_rules_plist_path) == True:
        #     # loading spec file
        #     specNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(build_rules_plist_path, Foundation.NSUncachedRead, None);
        #     if errorMessage == None:
        #         specString = Foundation.NSString.alloc().initWithData_encoding_(specNSData, Foundation.NSUTF8StringEncoding);
        #         if specString != None:
        #             contents = specString.propertyList();
        #         else:
        #             print 'Could not load string from data';
        #     else:
        #         print errorMessage;
        # else:
        #     print 'path does not exist!';
        
        compilers = self.getSpecForFilter(lambda spec: spec.type == 'Compiler' and spec.identifier.startswith('com.apple.compiler'));
        for compiler in filter(lambda compiler: ('IsAbstract' in compiler.contents.keys() and compiler.contents['IsAbstract'] == 'NO') or ('SynthesizeBuildRule' in compiler.contents.keys()), compilers):
            contents.append(xcbuildrule(compiler));
        
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
        
        return compiler;
        