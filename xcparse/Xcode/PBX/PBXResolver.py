import PBXBuildFile 
import PBXFileReference 
import PBXFrameworksBuildPhase 
import PBXGroup 
import PBXNativeTarget 
import PBXHeadersBuildPhase 
import XCConfigurationList 
import XCBuildConfiguration 
import PBXSourcesBuildPhase 
import PBXVariantGroup 
import PBXTargetDependency 
import PBXAggregateTarget 
import PBXApplicationTarget 
import PBXContainerItemProxy 
import PBXCopyFilesBuildPhase 
import PBXProject 
import PBXResourcesBuildPhase 
import PBXRezBuildPhase 
import PBXShellScriptBuildPhase 
import PBXReferenceProxy 
import PBXAppleScriptBuildPhase 
import PBXLegacyTarget 
import PBXJavaArchiveBuildPhase 
import PBXBundleTarget 
import PBXStandAloneTarget 
import PBXLibraryTarget 
import PBXFrameworkTarget 
import PBXBuildRule 
import PBXFrameworkReference 
import PBXApplicationReference 
import PBXExecutableFileReference 
import PBXLibraryReference 
import PBXBundleReference 
import PBXZipArchiveReference 

PBX_TYPE_RESOLVER = {
    'PBXBuildFile': PBXBuildFile.PBXBuildFile,
    'PBXFileReference': PBXFileReference.PBXFileReference,
    'PBXFrameworksBuildPhase': PBXFrameworksBuildPhase.PBXFrameworksBuildPhase,
    'PBXGroup': PBXGroup.PBXGroup,
    'PBXNativeTarget': PBXNativeTarget.PBXNativeTarget,
    'PBXHeadersBuildPhase': PBXHeadersBuildPhase.PBXHeadersBuildPhase,
    'XCConfigurationList': XCConfigurationList.XCConfigurationList,
    'XCBuildConfiguration': XCBuildConfiguration.XCBuildConfiguration,
    'PBXSourcesBuildPhase': PBXSourcesBuildPhase.PBXSourcesBuildPhase,
    'PBXVariantGroup': PBXVariantGroup.PBXVariantGroup,
    'PBXTargetDependency': PBXTargetDependency.PBXTargetDependency,
    'PBXAggregateTarget': PBXAggregateTarget.PBXAggregateTarget,
    'PBXApplicationTarget': PBXApplicationTarget.PBXApplicationTarget,
    'PBXContainerItemProxy': PBXContainerItemProxy.PBXContainerItemProxy,
    'PBXCopyFilesBuildPhase': PBXCopyFilesBuildPhase.PBXCopyFilesBuildPhase,
    'PBXProject': PBXProject.PBXProject,
    'PBXResourcesBuildPhase': PBXResourcesBuildPhase.PBXResourcesBuildPhase,
    'PBXRezBuildPhase': PBXRezBuildPhase.PBXRezBuildPhase,
    'PBXShellScriptBuildPhase': PBXShellScriptBuildPhase.PBXShellScriptBuildPhase,
    'PBXReferenceProxy': PBXReferenceProxy.PBXReferenceProxy,
    'PBXAppleScriptBuildPhase': PBXAppleScriptBuildPhase.PBXAppleScriptBuildPhase,
    'PBXLegacyTarget': PBXLegacyTarget.PBXLegacyTarget,
    'PBXJavaArchiveBuildPhase': PBXJavaArchiveBuildPhase.PBXJavaArchiveBuildPhase,
    'PBXBundleTarget': PBXBundleTarget.PBXBundleTarget,
    'PBXStandAloneTarget': PBXStandAloneTarget.PBXStandAloneTarget,
    'PBXLibraryTarget': PBXLibraryTarget.PBXLibraryTarget,
    'PBXFrameworkTarget': PBXFrameworkTarget.PBXFrameworkTarget,
    'PBXBuildRule': PBXBuildRule.PBXBuildRule,
    'PBXFrameworkReference': PBXFrameworkReference.PBXFrameworkReference,
    'PBXApplicationReference': PBXApplicationReference.PBXApplicationReference,
    'PBXExecutableFileReference': PBXExecutableFileReference.PBXExecutableFileReference,
    'PBXLibraryReference': PBXLibraryReference.PBXLibraryReference,
    'PBXBundleReference': PBXBundleReference.PBXBundleReference,
    'PBXZipArchiveReference': PBXZipArchiveReference.PBXZipArchiveReference,
};

def PBXResolver(dictionary):
    global PBX_TYPE_RESOLVER;
    if dictionary['isa'] in PBX_TYPE_RESOLVER.keys():
        return (True, PBX_TYPE_RESOLVER[dictionary['isa']]);
    else:
        print 'SKIPPING "%s" TYPE!' % dictionary['isa'];
    return (False, None);
