from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXBuildFile import *
from .PBXFileReference import *
from .PBXFrameworksBuildPhase import *
from .PBXGroup import *
from .PBXNativeTarget import *
from .PBXHeadersBuildPhase import *
from .XCConfigurationList import *
from .XCBuildConfiguration import *
from .PBXSourcesBuildPhase import *
from .PBXVariantGroup import *
from .PBXTargetDependency import *
from .PBXAggregateTarget import *
from .PBXApplicationTarget import *
from .PBXContainerItemProxy import *
from .PBXCopyFilesBuildPhase import *
from .PBXProject import *
from .PBXResourcesBuildPhase import *
from .PBXRezBuildPhase import *
from .PBXShellScriptBuildPhase import *
from .PBXReferenceProxy import *
from .PBXAppleScriptBuildPhase import *
from .PBXLegacyTarget import *
from .PBXJavaArchiveBuildPhase import *
from .PBXBundleTarget import *
from .PBXStandAloneTarget import *
from .PBXLibraryTarget import *
from .PBXFrameworkTarget import *
from .PBXBuildRule import *
from .PBXFrameworkReference import *
from .PBXApplicationReference import *
from .PBXExecutableFileReference import *
from .PBXLibraryReference import *
from .PBXBundleReference import *
from .PBXZipArchiveReference import *

PBX_TYPE_RESOLVER = {
    'PBXBuildFile': PBXBuildFile,
    'PBXFileReference': PBXFileReference,
    'PBXFrameworksBuildPhase': PBXFrameworksBuildPhase,
    'PBXGroup': PBXGroup,
    'PBXNativeTarget': PBXNativeTarget,
    'PBXHeadersBuildPhase': PBXHeadersBuildPhase,
    'XCConfigurationList': XCConfigurationList,
    'XCBuildConfiguration': XCBuildConfiguration,
    'PBXSourcesBuildPhase': PBXSourcesBuildPhase,
    'PBXVariantGroup': PBXVariantGroup,
    'PBXTargetDependency': PBXTargetDependency,
    'PBXAggregateTarget': PBXAggregateTarget,
    'PBXApplicationTarget': PBXApplicationTarget,
    'PBXContainerItemProxy': PBXContainerItemProxy,
    'PBXCopyFilesBuildPhase': PBXCopyFilesBuildPhase,
    'PBXProject': PBXProject,
    'PBXResourcesBuildPhase': PBXResourcesBuildPhase,
    'PBXRezBuildPhase': PBXRezBuildPhase,
    'PBXShellScriptBuildPhase': PBXShellScriptBuildPhase,
    'PBXReferenceProxy': PBXReferenceProxy,
    'PBXAppleScriptBuildPhase': PBXAppleScriptBuildPhase,
    'PBXLegacyTarget': PBXLegacyTarget,
    'PBXJavaArchiveBuildPhase': PBXJavaArchiveBuildPhase,
    'PBXBundleTarget': PBXBundleTarget,
    'PBXStandAloneTarget': PBXStandAloneTarget,
    'PBXLibraryTarget': PBXLibraryTarget,
    'PBXFrameworkTarget': PBXFrameworkTarget,
    'PBXBuildRule': PBXBuildRule,
    'PBXFrameworkReference': PBXFrameworkReference,
    'PBXApplicationReference': PBXApplicationReference,
    'PBXExecutableFileReference': PBXExecutableFileReference,
    'PBXLibraryReference': PBXLibraryReference,
    'PBXBundleReference': PBXBundleReference,
    'PBXZipArchiveReference': PBXZipArchiveReference,
};

def PBXResolver(dictionary):
    global PBX_TYPE_RESOLVER;
    if dictionary['isa'] in PBX_TYPE_RESOLVER.keys():
        return (True, PBX_TYPE_RESOLVER[dictionary['isa']]);
    else:
        print 'SKIPPING "%s" TYPE!' % dictionary['isa'];
    return (False, None);
