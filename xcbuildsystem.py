from __future__ import absolute_import
import os
import sys
import importlib

from .xcrun import *
from .xcspec import *

class xcbuildsystem(object):
    
    def __init__(self):
        self.specs = set();
        # loading default specs
        build_phase_types = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Built-in build phase types.xcspec');
        self.specs.update(build_phase_types);
        compilers = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Built-in compilers.pbcompspec');
        self.specs.update(compilers);
        languages = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Built-in languages.pblangspec');
        self.specs.update(languages);
        property_condition_flavors = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Built-in property condition flavors.xcspec');
        self.specs.update(property_condition_flavors);
        runtime_systems = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Built-in Runtime Systems.pbRTSspec');
        self.specs.update(runtime_systems);
        code_sign = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Code Sign.xcspec');
        self.specs.update(code_sign);
        core_build_system = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Core Build System.xcspec');
        self.specs.update(core_build_system);
        external_build_system = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/External Build System.xcspec');
        self.specs.update(external_build_system);
        jam_build_system = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Jam Build System.xcspec');
        self.specs.update(jam_build_system);
        native_build_system = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Native Build System.xcspec');
        self.specs.update(native_build_system);
        standard_file_types = xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/Standard file types.pbfilespec');
        self.specs.update(standard_file_types);
        #= xcspecLoadFileAtRelativeDeveloperPath('../OtherFrameworks/DevToolsCore.framework/Resources/');
    
    
    def getSpecForIdentifier(self, identifier):
        results = filter(lambda spec: spec.identifier == identifier, self.specs);
        if len(results) > 0:
            return results[0];
        else:
            return None;