from __future__ import absolute_import
from .xcspec import *
from ....Helpers import logging_helper

from .XCSpecCompiler import *
from .XCSpecProductType import *
from .XCSpecBuildStep import *
from .XCSpecBuildSettings import *
from .XCSpecFileType import *
from .XCSpecTool import *
from .XCSpecLinker import *
from .XCSpecBuildPhase import *
from .XCSpecBuildSystem import *
from .XCSpecPackageType import *
from .XCSpecArchitecture import *


XCSPEC_TYPE_RESOLVER = {
    'Compiler': XCSpecCompiler,
    'ProductType': XCSpecProductType,
    'BuildStep': XCSpecBuildStep,
    'BuildSettings': XCSpecBuildSettings,
    'FileType': XCSpecFileType,
    'Tool': XCSpecTool,
    'Linker': XCSpecLinker,
    'BuildPhase': XCSpecBuildPhase,
    'BuildSystem': XCSpecBuildSystem,
    'Architecture': XCSpecArchitecture,
    'PackageType': XCSpecPackageType,
};

def xcspec_resolver(dictionary):
    global XCSPEC_TYPE_RESOLVER;
    if dictionary['Type'] in XCSPEC_TYPE_RESOLVER.keys():
        return (True, XCSPEC_TYPE_RESOLVER[dictionary['Type']]);
    else:
        logging_helper.getLogger().warning('[xcspec_resolver]: UNKNOWN "%s" TYPE!' % dictionary['Type']);
    return (False, None);