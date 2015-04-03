from .EnvVarCondition import *
from ....Helpers import logging_helper
import objc

kENVIRONMENT_LOOKUP =  {
    'ACTION': 'String',
    'ADDITIONAL_SDKS': 'String',
    'ALTERNATE_GROUP': 'String',
    'ALTERNATE_MODE': 'String',
    'ALTERNATE_OWNER': 'String',
    'ALTERNATE_PERMISSIONS_FILES': 'StringList',
    'ALWAYS_SEARCH_USER_PATHS': 'Boolean',
    'APPLE_INTERNAL_DEVELOPER_DIR': 'Path',
    'APPLE_INTERNAL_DIR': 'Path',
    'APPLE_INTERNAL_DOCUMENTATION_DIR': 'Path',
    'APPLE_INTERNAL_LIBRARY_DIR': 'Path',
    'APPLE_INTERNAL_TOOLS': 'Path',
    'APPLICATION_EXTENSION_API_ONLY': 'Boolean',
    'APPLY_RULES_IN_COPY_FILES': 'Boolean',
    'ARCHS': 'String',
    'ARCHS_STANDARD': 'StringList',
    'ARCHS_STANDARD_32_64_BIT': 'StringList',
    'ARCHS_STANDARD_32_BIT': 'StringList',
    'ARCHS_STANDARD_64_BIT': 'StringList',
    'ARCHS_STANDARD_INCLUDING_64_BIT': 'StringList',
    'ARCHS_UNIVERSAL_IPHONE_OS': 'StringList',
    'ASSETCATALOG_COMPILER_APPICON_NAME': 'String',
    'ASSETCATALOG_COMPILER_LAUNCHIMAGE_NAME': 'String',
    'ASSETCATALOG_NOTICES': 'Boolean',
    'ASSETCATALOG_OTHER_FLAGS': 'StringList',
    'ASSETCATALOG_WARNINGS': 'Boolean',
    'AVAILABLE_PLATFORMS': 'String',
    'BUILD_COMPONENTS': 'String',
    'BUILD_DIR': 'Path',
    'BUILD_ROOT': 'Path',
    'BUILD_STYLE': 'String',
    'BUILD_VARIANTS': 'String',
    'BUILT_PRODUCTS_DIR': 'Path',
    'BUNDLE_LOADER': 'String',
    'CACHE_ROOT': 'Path',
    'CCHROOT': 'Path',
    'CHMOD': 'Path',
    'CHOWN': 'Path',
    'CLANG_ALLOW_NON_MODULAR_INCLUDES_IN_FRAMEWORK_MODULES': 'Boolean',
    'CLANG_ANALYZER_DEADCODE_DEADSTORES': 'Boolean',
    'CLANG_ANALYZER_GCD': 'Boolean',
    'CLANG_ANALYZER_MALLOC': 'Boolean',
    'CLANG_ANALYZER_MEMORY_MANAGEMENT': 'Boolean',
    'CLANG_ANALYZER_OBJC_ATSYNC': 'Boolean',
    'CLANG_ANALYZER_OBJC_COLLECTIONS': 'Boolean',
    'CLANG_ANALYZER_OBJC_INCOMP_METHOD_TYPES': 'Boolean',
    'CLANG_ANALYZER_OBJC_NSCFERROR': 'Boolean',
    'CLANG_ANALYZER_OBJC_RETAIN_COUNT': 'Boolean',
    'CLANG_ANALYZER_OBJC_SELF_INIT': 'Boolean',
    'CLANG_ANALYZER_OBJC_UNUSED_IVARS': 'Boolean',
    'CLANG_ANALYZER_SECURITY_FLOATLOOPCOUNTER': 'Boolean',
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_GETPW_GETS': 'Boolean',
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_MKSTEMP': 'Boolean',
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_RAND': 'Boolean',
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_STRCPY': 'Boolean',
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_UNCHECKEDRETURN': 'Boolean',
    'CLANG_ANALYZER_SECURITY_INSECUREAPI_VFORK': 'Boolean',
    'CLANG_ANALYZER_SECURITY_KEYCHAIN_API': 'Boolean',
    'CLANG_ARC_MIGRATE_DIR': 'Path',
    'CLANG_ARC_MIGRATE_EMIT_ERROR': 'Boolean',
    'CLANG_ARC_MIGRATE_PRECHECK': 'Enumeration',
    'CLANG_ARC_MIGRATE_REPORT_OUTPUT': 'Path',
    'CLANG_COLOR_DIAGNOSTICS': 'Boolean',
    'CLANG_CXX_LANGUAGE_STANDARD': 'Enumeration',
    'CLANG_CXX_LIBRARY': 'Enumeration',
    'CLANG_DEBUG_INFORMATION_LEVEL': 'Enumeration',
    'CLANG_ENABLE_APP_EXTENSION': 'Boolean',
    'CLANG_ENABLE_MODULES': 'Boolean',
    'CLANG_ENABLE_MODULE_IMPLEMENTATION_OF': 'Boolean',
    'CLANG_ENABLE_OBJC_ARC': 'Boolean',
    'CLANG_INSTRUMENT_FOR_OPTIMIZATION_PROFILING': 'Boolean',
    'CLANG_LINK_OBJC_RUNTIME': 'Boolean',
    'CLANG_MACRO_BACKTRACE_LIMIT': 'Integer',
    'CLANG_MODULES_AUTOLINK': 'Boolean',
    'CLANG_MODULES_IGNORE_MACROS': 'StringList',
    'CLANG_MODULES_VALIDATE_SYSTEM_HEADERS': 'Boolean',
    'CLANG_MODULES_VALIDATION_TIMESTAMP': 'String',
    'CLANG_MODULE_CACHE_PATH': 'Path',
    'CLANG_OBJC_MIGRATE_DIR': 'Path',
    'CLANG_OPTIMIZATION_PROFILE_FILE': 'Path',
    'CLANG_RETAIN_COMMENTS_FROM_SYSTEM_HEADERS': 'Boolean',
    'CLANG_STATIC_ANALYZER_MODE': 'Enumeration',
    'CLANG_STATIC_ANALYZER_MODE_ON_ANALYZE_ACTION': 'Enumeration',
    'CLANG_USE_OPTIMIZATION_PROFILE': 'Boolean',
    'CLANG_WARN_ASSIGN_ENUM': 'Boolean',
    'CLANG_WARN_BOOL_CONVERSION': 'Boolean',
    'CLANG_WARN_CONSTANT_CONVERSION': 'Boolean',
    'CLANG_WARN_CXX0X_EXTENSIONS': 'Boolean',
    'CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS': 'Boolean',
    'CLANG_WARN_DIRECT_OBJC_ISA_USAGE': 'Enumeration',
    'CLANG_WARN_DOCUMENTATION_COMMENTS': 'Boolean',
    'CLANG_WARN_EMPTY_BODY': 'Boolean',
    'CLANG_WARN_ENUM_CONVERSION': 'Boolean',
    'CLANG_WARN_IMPLICIT_SIGN_CONVERSION': 'Boolean',
    'CLANG_WARN_INT_CONVERSION': 'Boolean',
    'CLANG_WARN_OBJC_EXPLICIT_OWNERSHIP_TYPE': 'Boolean',
    'CLANG_WARN_OBJC_IMPLICIT_ATOMIC_PROPERTIES': 'Boolean',
    'CLANG_WARN_OBJC_IMPLICIT_RETAIN_SELF': 'Boolean',
    'CLANG_WARN_OBJC_MISSING_PROPERTY_SYNTHESIS': 'Boolean',
    'CLANG_WARN_OBJC_RECEIVER_WEAK': 'Boolean',
    'CLANG_WARN_OBJC_REPEATED_USE_OF_WEAK': 'Boolean',
    'CLANG_WARN_OBJC_ROOT_CLASS': 'Enumeration',
    'CLANG_WARN_SUSPICIOUS_IMPLICIT_CONVERSION': 'Boolean',
    'CLANG_WARN_UNREACHABLE_CODE': 'Boolean',
    'CLANG_WARN__ARC_BRIDGE_CAST_NONARC': 'Boolean',
    'CLANG_WARN__DUPLICATE_METHOD_MATCH': 'Boolean',
    'CLANG_WARN__EXIT_TIME_DESTRUCTORS': 'Boolean',
    'CLANG_X86_VECTOR_INSTRUCTIONS': 'Enumeration',
    'CODE_SIGN_ENTITLEMENTS': 'String',
    'CODE_SIGN_IDENTITY': 'String',
    'CODE_SIGN_RESOURCE_RULES_PATH': 'Path',
    'COLOR_DIAGNOSTICS': 'Boolean',
    'COMBINE_HIDPI_IMAGES': 'Boolean',
    'COMPOSITE_SDK_DIRS': 'PathList',
    'COMPRESS_PNG_FILES': 'Boolean',
    'CONFIGURATION': 'String',
    'CONFIGURATION_BUILD_DIR': 'Path',
    'CONFIGURATION_TEMP_DIR': 'Path',
    'COPYING_PRESERVES_HFS_DATA': 'Boolean',
    'COPY_PHASE_STRIP': 'Boolean',
    'CP': 'Path',
    'CPP_HEADERMAP_FILE': 'Path',
    'CPP_HEADERMAP_FILE_FOR_ALL_NON_FRAMEWORK_TARGET_HEADERS': 'Path',
    'CPP_HEADERMAP_FILE_FOR_ALL_TARGET_HEADERS': 'Path',
    'CPP_HEADERMAP_FILE_FOR_GENERATED_FILES': 'Path',
    'CPP_HEADERMAP_FILE_FOR_OWN_TARGET_HEADERS': 'Path',
    'CPP_HEADERMAP_FILE_FOR_PROJECT_FILES': 'Path',
    'CPP_HEADERMAP_PRODUCT_HEADERS_VFS_FILE': 'Path',
    'CPP_HEADER_SYMLINKS_DIR': 'Path',
    'CREATE_INFOPLIST_SECTION_IN_BINARY': 'Boolean',
    'CURRENT_ARCH': 'String',
    'CURRENT_PROJECT_VERSION': 'String',
    'CURRENT_VARIANT': 'String',
    'DEAD_CODE_STRIPPING': 'Boolean',
    'DEBUG_INFORMATION_FORMAT': 'String',
    'DEFAULT_COMPILER': 'String',
    'DEFAULT_KEXT_INSTALL_PATH': 'String',
    'DEFAULT_SSE_LEVEL_3_NO': 'String',
    'DEFAULT_SSE_LEVEL_3_YES': 'String',
    'DEFAULT_SSE_LEVEL_3_SUPPLEMENTAL_NO': 'String',
    'DEFAULT_SSE_LEVEL_3_SUPPLEMENTAL_YES': 'String',
    'DEFAULT_SSE_LEVEL_4_1_NO': 'String',
    'DEFAULT_SSE_LEVEL_4_1_YES': 'String',
    'DEFAULT_SSE_LEVEL_4_2_NO': 'String',
    'DEFAULT_SSE_LEVEL_4_2_YES': 'String',
    'DEFINES_MODULE': 'Boolean',
    'DEPLOYMENT_LOCATION': 'Boolean',
    'DEPLOYMENT_POSTPROCESSING': 'Boolean',
    'DERIVED_FILE_DIR': 'Path',
    'DERIVED_FILES_DIR': 'Path',
    'DERIVED_SOURCES_DIR': 'Path',
    'DEVELOPER_APPLICATIONS_DIR': 'Path',
    'DEVELOPER_BIN_DIR': 'Path',
    'DEVELOPER_DIR': 'Path',
    'DEVELOPER_FRAMEWORKS_DIR': 'Path',
    'DEVELOPER_FRAMEWORKS_DIR_QUOTED': 'Path',
    'DEVELOPER_LIBRARY_DIR': 'Path',
    'DEVELOPER_SDK_DIR': 'Path',
    'DEVELOPER_TOOLS_DIR': 'Path',
    'DEVELOPER_USR_DIR': 'Path',
    'DSTROOT': 'Path',
    'DT_TOOLCHAIN_DIR': 'Path',
    'DYLIB_COMPATIBILITY_VERSION': 'String',
    'DYLIB_CURRENT_VERSION': 'String',
    'DYLIB_INSTALL_NAME_BASE': 'StringList',
    'EFFECTIVE_PLATFORM_NAME': 'String',
    'EMBEDDED_CONTENT_CONTAINS_SWIFT': 'Boolean',
    'EMBEDDED_PROFILE_NAME': 'String',
    'ENABLE_APPLE_KEXT_CODE_GENERATION': 'Boolean',
    'ENABLE_HEADER_DEPENDENCIES': 'Boolean',
    'ENABLE_NS_ASSERTIONS': 'Boolean',
    'ENABLE_STRICT_OBJC_MSGSEND': 'Boolean',
    'EXCLUDED_INSTALLSRC_SUBDIRECTORY_PATTERNS': 'StringList',
    'EXCLUDED_RECURSIVE_SEARCH_PATH_SUBDIRECTORIES': 'StringList',
    'EXECUTABLE_EXTENSION': 'String',
    'EXECUTABLE_PREFIX': 'String',
    'EXECUTABLE_SUFFIX': 'String',
    'EXECUTABLE_VARIANT_SUFFIX': 'String',
    'EXPORTED_SYMBOLS_FILE': 'Path',
    'FILE_LIST': 'Path',
    'FRAMEWORK_SEARCH_PATHS': 'PathList',
    'FRAMEWORK_VERSION': 'String',
    'GCC3_VERSION': 'String',
    'GCC_CHAR_IS_UNSIGNED_CHAR': 'Boolean',
    'GCC_CW_ASM_SYNTAX': 'Boolean',
    'GCC_C_LANGUAGE_STANDARD': 'Enumeration',
    'GCC_DEBUG_INFORMATION_FORMAT': 'Enumeration',
    'GCC_DYNAMIC_NO_PIC': 'Boolean',
    'GCC_ENABLE_ASM_KEYWORD': 'Boolean',
    'GCC_ENABLE_BUILTIN_FUNCTIONS': 'Boolean',
    'GCC_ENABLE_CPP_EXCEPTIONS': 'Boolean',
    'GCC_ENABLE_CPP_RTTI': 'Boolean',
    'GCC_ENABLE_EXCEPTIONS': 'Boolean',
    'GCC_ENABLE_FLOATING_POINT_LIBRARY_CALLS': 'Boolean',
    'GCC_ENABLE_KERNEL_DEVELOPMENT': 'Boolean',
    'GCC_ENABLE_OBJC_EXCEPTIONS': 'Boolean',
    'GCC_ENABLE_OBJC_GC': 'Enumeration',
    'GCC_ENABLE_PASCAL_STRINGS': 'Boolean',
    'GCC_ENABLE_SSE3_EXTENSIONS': 'Boolean',
    'GCC_ENABLE_SSE41_EXTENSIONS': 'Boolean',
    'GCC_ENABLE_SSE42_EXTENSIONS': 'Boolean',
    'GCC_ENABLE_SUPPLEMENTAL_SSE3_INSTRUCTIONS': 'Boolean',
    'GCC_ENABLE_TRIGRAPHS': 'Boolean',
    'GCC_FAST_MATH': 'Boolean',
    'GCC_GENERATE_DEBUGGING_SYMBOLS': 'Boolean',
    'GCC_GENERATE_TEST_COVERAGE_FILES': 'Boolean',
    'GCC_INCREASE_PRECOMPILED_HEADER_SHARING': 'Boolean',
    'GCC_INLINES_ARE_PRIVATE_EXTERN': 'Boolean',
    'GCC_INPUT_FILETYPE': 'Enumeration',
    'GCC_INSTRUMENT_PROGRAM_FLOW_ARCS': 'Boolean',
    'GCC_LINK_WITH_DYNAMIC_LIBRARIES': 'Boolean',
    'GCC_MACOSX_VERSION_MIN': 'String',
    'GCC_NO_COMMON_BLOCKS': 'Boolean',
    'GCC_OBJC_ABI_VERSION': 'Enumeration',
    'GCC_OBJC_LEGACY_DISPATCH': 'Boolean',
    'GCC_OPERATION': 'Enumeration',
    'GCC_OPTIMIZATION_LEVEL': 'Enumeration',
    'GCC_PFE_FILE_C_DIALECTS': 'StringList',
    'GCC_PRECOMPILE_PREFIX_HEADER': 'Boolean',
    'GCC_PREFIX_HEADER': 'String',
    'GCC_PREPROCESSOR_DEFINITIONS': 'StringList',
    'GCC_PREPROCESSOR_DEFINITIONS_NOT_USED_IN_PRECOMPS': 'StringList',
    'GCC_PRODUCT_TYPE_PREPROCESSOR_DEFINITIONS': 'StringList',
    'GCC_REUSE_STRINGS': 'Boolean',
    'GCC_SHORT_ENUMS': 'Boolean',
    'GCC_STRICT_ALIASING': 'Boolean',
    'GCC_SYMBOLS_PRIVATE_EXTERN': 'Boolean',
    'GCC_THREADSAFE_STATICS': 'Boolean',
    'GCC_TREAT_IMPLICIT_FUNCTION_DECLARATIONS_AS_ERRORS': 'Boolean',
    'GCC_TREAT_INCOMPATIBLE_POINTER_TYPE_WARNINGS_AS_ERRORS': 'Boolean',
    'GCC_TREAT_WARNINGS_AS_ERRORS': 'Boolean',
    'GCC_UNROLL_LOOPS': 'Boolean',
    'GCC_USE_GCC3_PFE_SUPPORT': 'Boolean',
    'GCC_USE_STANDARD_INCLUDE_SEARCHING': 'Boolean',
    'GCC_VERSION': 'String',
    'GCC_WARN_64_TO_32_BIT_CONVERSION': 'Boolean',
    'GCC_WARN_ABOUT_DEPRECATED_FUNCTIONS': 'Boolean',
    'GCC_WARN_ABOUT_INVALID_OFFSETOF_MACRO': 'Boolean',
    'GCC_WARN_ABOUT_MISSING_FIELD_INITIALIZERS': 'Boolean',
    'GCC_WARN_ABOUT_MISSING_NEWLINE': 'Boolean',
    'GCC_WARN_ABOUT_MISSING_PROTOTYPES': 'Boolean',
    'GCC_WARN_ABOUT_POINTER_SIGNEDNESS': 'Boolean',
    'GCC_WARN_ABOUT_RETURN_TYPE': 'Enumeration',
    'GCC_WARN_ALLOW_INCOMPLETE_PROTOCOL': 'Boolean',
    'GCC_WARN_CHECK_SWITCH_STATEMENTS': 'Boolean',
    'GCC_WARN_FOUR_CHARACTER_CONSTANTS': 'Boolean',
    'GCC_WARN_HIDDEN_VIRTUAL_FUNCTIONS': 'Boolean',
    'GCC_WARN_INHIBIT_ALL_WARNINGS': 'Boolean',
    'GCC_WARN_INITIALIZER_NOT_FULLY_BRACKETED': 'Boolean',
    'GCC_WARN_MISSING_PARENTHESES': 'Boolean',
    'GCC_WARN_MULTIPLE_DEFINITION_TYPES_FOR_SELECTOR': 'Boolean',
    'GCC_WARN_NON_VIRTUAL_DESTRUCTOR': 'Boolean',
    'GCC_WARN_PEDANTIC': 'Boolean',
    'GCC_WARN_SHADOW': 'Boolean',
    'GCC_WARN_SIGN_COMPARE': 'Boolean',
    'GCC_WARN_STRICT_SELECTOR_MATCH': 'Boolean',
    'GCC_WARN_TYPECHECK_CALLS_TO_PRINTF': 'Boolean',
    'GCC_WARN_UNDECLARED_SELECTOR': 'Boolean',
    'GCC_WARN_UNINITIALIZED_AUTOS': 'Enumeration',
    'GCC_WARN_UNKNOWN_PRAGMAS': 'Boolean',
    'GCC_WARN_UNUSED_FUNCTION': 'Boolean',
    'GCC_WARN_UNUSED_LABEL': 'Boolean',
    'GCC_WARN_UNUSED_PARAMETER': 'Boolean',
    'GCC_WARN_UNUSED_VALUE': 'Boolean',
    'GCC_WARN_UNUSED_VARIABLE': 'Boolean',
    'GENERATE_MASTER_OBJECT_FILE': 'Boolean',
    'GENERATE_PKGINFO_FILE': 'Boolean',
    'GENERATE_PROFILING_CODE': 'Boolean',
    'GID': 'String',
    'GROUP': 'String',
    'HEADERMAP_FILE_FORMAT': 'Enumeration',
    'HEADERMAP_INCLUDES_FLAT_ENTRIES_FOR_TARGET_BEING_BUILT': 'Boolean',
    'HEADERMAP_INCLUDES_FRAMEWORK_ENTRIES_FOR_ALL_PRODUCT_TYPES': 'Boolean',
    'HEADERMAP_INCLUDES_NONPUBLIC_NONPRIVATE_HEADERS': 'Boolean',
    'HEADERMAP_INCLUDES_PROJECT_HEADERS': 'Boolean',
    'HEADERMAP_USES_FRAMEWORK_PREFIX_ENTRIES': 'Boolean',
    'HEADERMAP_USES_VFS': 'Boolean',
    'HEADER_SEARCH_PATHS': 'PathList',
    'IBC_COMPILER_AUTO_ACTIVATE_CUSTOM_FONTS': 'Boolean',
    'IBC_ERRORS': 'Boolean',
    'IBC_FLATTEN_NIBS': 'Boolean',
    'IBC_NOTICES': 'Boolean',
    'IBC_OTHER_FLAGS': 'StringList',
    'IBC_WARNINGS': 'Boolean',
    'ICONV': 'Path',
    'INCLUDED_RECURSIVE_SEARCH_PATH_SUBDIRECTORIES': 'StringList',
    'INFOPLIST_EXPAND_BUILD_SETTINGS': 'Boolean',
    'INFOPLIST_FILE': 'Path',
    'INFOPLIST_OTHER_PREPROCESSOR_FLAGS': 'StringList',
    'INFOPLIST_OUTPUT_FORMAT': 'Enumeration',
    'INFOPLIST_PREFIX_HEADER': 'String',
    'INFOPLIST_PREPROCESS': 'Boolean',
    'INFOPLIST_PREPROCESSOR_DEFINITIONS': 'StringList',
    'INIT_ROUTINE': 'String',
    'INSTALL_DIR': 'Path',
    'INSTALL_GROUP': 'String',
    'INSTALL_MODE_FLAG': 'String',
    'INSTALL_OWNER': 'String',
    'INSTALL_PATH': 'Path',
    'INSTALL_ROOT': 'Path',
    'IPHONEOS_DEPLOYMENT_TARGET': 'String',
    'JAVAC_DEFAULT_FLAGS': 'String',
    'JAVA_APP_STUB': 'Path',
    'JAVA_ARCHIVE_CLASSES': 'Boolean',
    'JAVA_ARCHIVE_TYPE': 'Enumeration',
    'JAVA_COMPILER': 'Path',
    'JAVA_FRAMEWORK_RESOURCES_DIRS': 'PathList',
    'JAVA_JAR_FLAGS': 'StringList',
    'JAVA_SOURCE_SUBDIR': 'Path',
    'JAVA_USE_DEPENDENCIES': 'Boolean',
    'JAVA_ZIP_FLAGS': 'StringList',
    'KEEP_PRIVATE_EXTERNS': 'Boolean',
    'LD_DEPENDENCY_INFO_FILE': 'Path',
    'LD_DYLIB_INSTALL_NAME': 'Path',
    'LD_GENERATE_MAP_FILE': 'Boolean',
    'LD_MAP_FILE_PATH': 'Path',
    'LD_NO_PIE': 'Boolean',
    'LD_QUOTE_LINKER_ARGUMENTS_FOR_COMPILER_DRIVER': 'Boolean',
    'LD_RUNPATH_SEARCH_PATHS': 'StringList',
    'LEGACY_DEVELOPER_DIR': 'Path',
    'LEX': 'Path',
    'LEXFLAGS': 'StringList',
    'LIBRARY_FLAG_NOSPACE': 'Boolean',
    'LIBRARY_FLAG_PREFIX': 'String',
    'LIBRARY_KEXT_INSTALL_PATH': 'Path',
    'LIBRARY_SEARCH_PATHS': 'PathList',
    'LINKER_DISPLAYS_MANGLED_NAMES': 'Boolean',
    'LINK_WITH_STANDARD_LIBRARIES': 'Boolean',
    'LLVM_IMPLICIT_AGGRESSIVE_OPTIMIZATIONS': 'Boolean',
    'LLVM_LTO': 'Boolean',
    'LLVM_OPTIMIZATION_LEVEL_VAL_0': 'Boolean',
    'LLVM_OPTIMIZATION_LEVEL_VAL_1': 'Boolean',
    'LLVM_OPTIMIZATION_LEVEL_VAL_2': 'Boolean',
    'LLVM_OPTIMIZATION_LEVEL_VAL_3': 'Boolean',
    'LLVM_OPTIMIZATION_LEVEL_VAL_fast': 'Boolean',
    'LLVM_OPTIMIZATION_LEVEL_VAL_s': 'Boolean',
    'LOCAL_ADMIN_APPS_DIR': 'Path',
    'LOCAL_APPS_DIR': 'Path',
    'LOCAL_DEVELOPER_DIR': 'Path',
    'LOCAL_LIBRARY_DIR': 'Path',
    'MACH_O_TYPE': 'Enumeration',
    'MACOSX_DEPLOYMENT_TARGET': 'Enumeration',
    'MODULEMAP_FILE': 'String',
    'MODULEMAP_PRIVATE_FILE': 'String',
    'MODULE_CACHE_DIR': 'Path',
    'MODULE_NAME': 'String',
    'MODULE_START': 'String',
    'MODULE_STOP': 'String',
    'MODULE_VERSION': 'String',
    'MTL_ENABLE_DEBUG_INFO': 'Boolean',
    'NATIVE_ARCH': 'String',
    'OBJC_ABI_VERSION': 'String',
    'OBJECT_FILE_DIR': 'Path',
    'OBJECT_FILE_DIR_': 'Path',
    'OBJROOT': 'Path',
    'ONLY_ACTIVE_ARCH': 'Boolean',
    'ORDER_FILE': 'String',
    'OS': 'String',
    'OSAC': 'Path',
    'OSACOMPILE_EXECUTE_ONLY': 'Boolean',
    'OTHER_CFLAGS': 'StringList',
    'OTHER_CODE_SIGN_FLAGS': 'StringList',
    'OTHER_CPLUSPLUSFLAGS': 'StringList',
    'OTHER_LDFLAGS': 'StringList',
    'OTHER_LIBTOOLFLAGS': 'StringList',
    'OTHER_OSACOMPILEFLAGS': 'String',
    'PATH_PREFIXES_EXCLUDED_FROM_HEADER_DEPENDENCIES': 'PathList',
    'PLATFORM_DEVELOPER_APPLICATIONS_DIR': 'Path',
    'PLATFORM_DEVELOPER_BIN_DIR': 'Path',
    'PLATFORM_DEVELOPER_LIBRARY_DIR': 'Path',
    'PLATFORM_DEVELOPER_SDK_DIR': 'Path',
    'PLATFORM_DEVELOPER_TOOLS_DIR': 'String',
    'PLATFORM_DEVELOPER_USR_DIR': 'Path',
    'PLATFORM_DIR': 'Path',
    'PLATFORM_NAME': 'String',
    'PLATFORM_PREFERRED_ARCH': 'String',
    'PLATFORM_PRODUCT_BUILD_VERSION': 'String',
    'PLIST_FILE_OUTPUT_FORMAT': 'Enumeration',
    'PRECOMPILE_PREFIX_HEADER': 'Boolean',
    'PRECOMPS_INCLUDE_HEADERS_FROM_BUILT_PRODUCTS_DIR': 'Boolean',
    'PREFIX_HEADER': 'Path',
    'PRELINK_FLAGS': 'StringList',
    'PRELINK_LIBS': 'StringList',
    'PRESERVE_DEAD_CODE_INITS_AND_TERMS': 'Boolean',
    'PRIVATE_HEADERS_FOLDER_PATH': 'Path',
    'PRODUCT_DEFINITION_PLIST': 'String',
    'PRODUCT_MODULE_NAME': 'String',
    'PRODUCT_NAME': 'String',
    'PROJECT': 'String',
    'PROJECT_DERIVED_FILE_DIR': 'Path',
    'PROJECT_DIR': 'Path',
    'PROJECT_FILE_PATH': 'Path',
    'PROJECT_NAME': 'String',
    'PROJECT_TEMP_DIR': 'Path',
    'PROJECT_TEMP_ROOT': 'Path',
    'PROVISIONING_PROFILE': 'String',
    'PUBLIC_HEADERS_FOLDER_PATH': 'Path',
    'REMOVE_CVS_FROM_RESOURCES': 'Boolean',
    'REMOVE_GIT_FROM_RESOURCES': 'Boolean',
    'REMOVE_HEADERS_FROM_EMBEDDED_BUNDLES': 'Boolean',
    'REMOVE_HG_FROM_RESOURCES': 'Boolean',
    'REMOVE_SVN_FROM_RESOURCES': 'Boolean',
    'RETAIN_RAW_BINARIES': 'Boolean',
    'REZ_COLLECTOR_DIR': 'Path',
    'REZ_OBJECTS_DIR': 'Path',
    'REZ_SEARCH_PATHS': 'String',
    'RUN_CLANG_STATIC_ANALYZER': 'Boolean',
    'SCAN_ALL_SOURCE_FILES_FOR_INCLUDES': 'Boolean',
    'SDKROOT': 'String',
    'SDK_DIR': 'Path',
    'SDK_NAME': 'String',
    'SDK_PRODUCT_BUILD_VERSION': 'String',
    'SECTORDER_FLAGS': 'StringList',
    'SED': 'Path',
    'SEPARATE_STRIP': 'Boolean',
    'SEPARATE_SYMBOL_EDIT': 'Boolean',
    'SHARED_PRECOMPS_DIR': 'Path',
    'SKIP_INSTALL': 'Boolean',
    'SOURCE_ROOT': 'Path',
    'SRCROOT': 'Path',
    'STRINGS_FILE_OUTPUT_ENCODING': 'String',
    'STRIPFLAGS': 'Boolean',
    'STRIP_INSTALLED_PRODUCT': 'Boolean',
    'STRIP_STYLE': 'Enumeration',
    'SUPPORTED_PLATFORMS': 'StringList',
    'SWIFT_OPTIMIZATION_LEVEL': 'Enumeration',
    'SYMROOT': 'Path',
    'SYSTEM_ADMIN_APPS_DIR': 'Path',
    'SYSTEM_APPS_DIR': 'Path',
    'SYSTEM_CORE_SERVICES_DIR': 'Path',
    'SYSTEM_DEMOS_DIR': 'Path',
    'SYSTEM_DEVELOPER_APPS_DIR': 'Path',
    'SYSTEM_DEVELOPER_BIN_DIR': 'Path',
    'SYSTEM_DEVELOPER_DEMOS_DIR': 'Path',
    'SYSTEM_DEVELOPER_DIR': 'Path',
    'SYSTEM_DEVELOPER_DOC_DIR': 'Path',
    'SYSTEM_DEVELOPER_GRAPHICS_TOOLS_DIR': 'Path',
    'SYSTEM_DEVELOPER_JAVA_TOOLS_DIR': 'Path',
    'SYSTEM_DEVELOPER_PERFORMANCE_TOOLS_DIR': 'Path',
    'SYSTEM_DEVELOPER_RELEASENOTES_DIR': 'Path',
    'SYSTEM_DEVELOPER_TOOLS': 'Path',
    'SYSTEM_DEVELOPER_TOOLS_DOC_DIR': 'Path',
    'SYSTEM_DEVELOPER_TOOLS_RELEASENOTES_DIR': 'Path',
    'SYSTEM_DEVELOPER_USR_DIR': 'Path',
    'SYSTEM_DEVELOPER_UTILITIES_DIR': 'Path',
    'SYSTEM_DOCUMENTATION_DIR': 'Path',
    'SYSTEM_KEXT_INSTALL_PATH': 'Path',
    'SYSTEM_LIBRARY_DIR': 'Path',
    'TARGETNAME': 'String',
    'TARGET_BUILD_DIR': 'Path',
    'TARGET_NAME': 'String',
    'TARGET_TEMP_DIR': 'Path',
    'TARGETED_DEVICE_FAMILY': 'String',
    'TEMP_DIR': 'Path',
    'TEMP_FILES_DIR': 'Path',
    'TEMP_FILE_DIR': 'Path',
    'TEMP_ROOT': 'Path',
    'TEST_HOST': 'String',
    'TREAT_MISSING_BASELINES_AS_TEST_FAILURES': 'Boolean',
    'UID': 'String',
    'UNEXPORTED_SYMBOLS_FILE': 'String',
    'UNSTRIPPED_PRODUCT': 'Boolean',
    'USER': 'String',
    'USER_APPS_DIR': 'Path',
    'USER_HEADER_SEARCH_PATHS': 'PathList',
    'USER_LIBRARY_DIR': 'Path',
    'USE_HEADERMAP': 'Boolean',
    'USE_HEADER_SYMLINKS': 'Boolean',
    'VALIDATE_PRODUCT': 'Boolean',
    'VALID_ARCHS': 'StringList',
    'VERSIONING_SYSTEM': 'String',
    'VERSION_INFO_BUILDER': 'String',
    'VERSION_INFO_EXPORT_DECL': 'String',
    'VERSION_INFO_FILE': 'String',
    'VERSION_INFO_PREFIX': 'String',
    'VERSION_INFO_SUFFIX': 'String',
    'WARNING_CFLAGS': 'StringList',
    'WARNING_LDFLAGS': 'StringList',
    'WRAPPER_EXTENSION': 'String',
    'XCODE_APP_SUPPORT_DIR': 'Path',
    'XCODE_PRODUCT_BUILD_VERSION': 'String',
    'XCODE_VERSION_ACTUAL': 'String',
    'XCODE_VERSION_MAJOR': 'String',
    'XCODE_VERSION_MINOR': 'String',
    'YACC': 'Path',
    'YACCFLAGS': 'StringList',
};


class EnvVariable(object):
    
    def __init__(self, dictionary):
        if 'Name' in dictionary.keys():
            self.name = dictionary['Name'];
        if self.name in kENVIRONMENT_LOOKUP.keys():
            self.Type = kENVIRONMENT_LOOKUP[self.name];
        else:
            self.Type = 'String'; # unknown default for now
        if 'Type' in dictionary.keys():
            self.Type = dictionary['Type'];
        if 'DefaultValue' in dictionary.keys():
            self.DefaultValue = dictionary['DefaultValue'];
        else:
            default_values = {
                'Boolean': 'NO',
                'Bool': 'NO',
                'bool': 'NO',
                
                'String': '',
                'string': '',
                
                'Enumeration': '',
                'enum': '',
                
                'PathList': '',
                'pathlist': '',
                
                'Path': '',
                'path': '',
                
                'StringList': '',
                'stringlist': '',
            };
            
            if self.Type in default_values:
                self.DefaultValue = default_values[self.Type];
            else:
                logging_helper.getLogger().warning('[EnvVariable]: type not found %s' % (self.Type));
        self.values = set();
        self.mergeDefinition(dictionary);
    
    # def __attrs(self):
    #     return (self.name, self.type);
    #
    def __repr__(self):
        return '(%s : %s : %s : %s - %s)' % (type(self), self.name, self.Type, self.DefaultValue, self.values);
    
    # def __eq__(self, other):
    #     return isinstance(other, type(self)) and self.name == other.name and self.Type == other.Type;
    #
    # def __hash__(self):
    #     return hash(self.__attrs());
    
    def isList(self):
        return self.Type in ['stringlist', 'StringList', 'pathlist', 'PathList'];
    
    def isPath(self):
        return self.Type in ['path', 'Path', 'pathlist', 'PathList'];
    
    def isString(self):
        return self.Type in ['string', 'String', 'stringlist', 'StringList'];
    
    def isBoolean(self):
        return self.Type in ['Boolean', 'bool', 'Bool'];
    
    def isEnum(self):
        return self.Type in ['enum', 'Enumeration'];
    
    def mergeDefinition(self, dictionary, aggressive=True):
        for key in dictionary.keys():
            if hasattr(self, key) == False:
                setattr(self, key, dictionary[key]);
            else:
                if dictionary[key] != getattr(self, key) and aggressive == True:
                    setattr(self, key, dictionary[key]);
    
    def addConditionalValue(self, conditional):
        if len(conditional.keys) == 0:
            self.DefaultValue = conditional.value;
        self.values.add(conditional);
    
    def satisfiesCondition(self, environment):
        if hasattr(self, 'Condition') == True:
            expression = str(environment.parseKey(self.Condition)[1]);
            expression_list = expression.split(' ');
            list_filter_yes = map(lambda item: 'True' if item == 'YES' else item, expression_list);
            list_filter_no = map(lambda item: 'False' if item == 'NO' else item, list_filter_yes);
            list_filter_not = map(lambda item: 'not' if item == '!' else item, list_filter_no);
            list_filter_and = map(lambda item: 'and' if item == '&&' else item, list_filter_not);
            list_filter_or = map(lambda item: 'or' if item == '||' else item, list_filter_and);
            list_filter_strings = map(lambda item: '"'+item+'"' if item not in ['True', 'False', 'not', 'and', 'or', '==', '!='] and not item.startswith('\\"') else item, list_filter_or);
            eval_string = ' '.join(list_filter_strings).replace('\\"', '"');
            return eval(eval_string);
        else:
            return True;
    
    def value(self, environment):
        result_value = self.DefaultValue;
        for conditional in self.values:
            if conditional.evaluate(environment) == True:
                result_value = conditional.value;
                break;
        # add check for parsing the value if necessary
        if type(result_value) is unicode:
            result_value = str(result_value);
        if type(result_value) is objc.pyobjc_unicode:
            result_value = str(result_value);
        if type(result_value) is str:
            test_result_value = environment.parseKey(result_value, 'target', environment.resolvedValues());
            if test_result_value[0] == True:
                result_value = test_result_value[1];
            else:
                logging_helper.getLogger().error('[EnvVariable]: BAD VARIABLE :(');
        else:
            result_str = '';
            for item in result_value:
                result_str += str(item)+' ';
            result_value = result_str;
        if '$(inherited)' in result_value:
            # is this correct
            current_level = environment.levelForVariable(self);
            if current_level[0] == True:
                index = environment.levels_order[current_level[1]] - 1;
                inherited_value = ' ';
                if index >= 0:
                    inherited_value = environment.parseKey(result_value, environment.levels_lookup[index])[1];
            result_value = result_value.replace('$(inherited)', inherited_value);
        return result_value;
    
    def hasCommandLineArgs(self):
        return hasattr(self, 'CommandLinePrefixFlag') or hasattr(self, 'CommandLineArgs');
    
    def commandLineFlag(self, environment):
        output = '';
        
        prefix_flag = '';
        if hasattr(self, 'CommandLinePrefixFlag') == True:
            prefix_flag = self.CommandLinePrefixFlag;
        
        primary_flag = '';
        flag_lookup_keys = [];
        flag_lookup_values = {};
        if hasattr(self, 'CommandLineArgs') == True:
            if hasattr(self.CommandLineArgs, 'keys') and callable(getattr(self.CommandLineArgs, 'keys')):
                for key in self.CommandLineArgs.keys():
                    flag_lookup_values[str(key)] = self.CommandLineArgs[key];
                flag_lookup_keys = list(map(lambda item: str(item), self.CommandLineArgs.keys()));
            elif len(self.CommandLineArgs) > 0:
                args_list = map(lambda item: str(item), self.CommandLineArgs);
                if hasattr(self, 'AllowedValues') == True:
                    flag_lookup_keys = list(map(lambda item: str(item), getattr(self, 'AllowedValues')));
                    for key in flag_lookup_keys:
                        flag_lookup_values[str(key)] = args_list
                else:
                    primary_flag = ' '.join(args_list);
        
        flag_list = [];
        
        
        value = self.value(environment);
        if self.isList():
            value_list = filter(lambda item: len(item) > 0, value.split(' '));
            if len(flag_lookup_keys) > 0:
                if value in flag_lookup_values.keys():
                    flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                elif '<<otherwise>>' in flag_lookup_keys:
                    flag_list = map(lambda item: str(item), flag_lookup_values['<<otherwise>>']);
                else:
                    logging_helper.getLogger().warn('[EnvVariable]: Error in parsing flag_lookup_values: %s' % flag_lookup_values);
            else:
                # use primary flag
                for item in value_list:
                    flag_list.append(primary_flag.replace('$(value)', item));
        elif self.isString() or self.isPath():
            value = str(value);
            if len(flag_lookup_values) > 0:
                if value in flag_lookup_values.keys():
                    flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                elif '<<otherwise>>' in flag_lookup_keys:
                    flag_list = map(lambda item: str(item), flag_lookup_values['<<otherwise>>']);
                else:
                    logging_helper.getLogger().warn('[EnvVariable]: Error in parsing flag_lookup_values: %s' % flag_lookup_values);
            else:
                # prefix flag check
                flag_list.append(prefix_flag.replace('$(value)', value)+value);
        elif self.isBoolean():
            value = str(value);
            if value in flag_lookup_keys:
                flag_list = map(lambda item: str(item), flag_lookup_values[value]);
        elif self.isEnum():
            value = str(value);
            if hasattr(self, 'AllowedValues') == True:
                value_list = list(map(lambda item: str(item), getattr(self, 'AllowedValues')));
                if value in value_list and value in flag_lookup_values.keys():
                    flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                elif value in flag_lookup_values.keys():
                    flag_list = map(lambda item: str(item), flag_lookup_values[value]);
                elif '<<otherwise>>' in flag_lookup_keys:
                    flag_list = map(lambda item: str(item), flag_lookup_values['<<otherwise>>']);
                else:
                    logging_helper.getLogger().error('[EnvVariable]: Value %s not allowed (%s) for %s' % (value, str(value_list), self.name));
            else:
                logging_helper.getLogger().warn('[EnvVariable]: Could not find "AllowedValues" on %s' % self.name);
        else:
            logging_helper.getLogger().error('[EnvVariable]: Unknown variable type!');
        
        output = ' '.join(map(lambda item: item.replace('$(value)', value), flag_list));
        
        output = environment.parseKey(output)[1];
        return output;