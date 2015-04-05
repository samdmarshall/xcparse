import os
from .EnvVarCondition import *
from .EnvVariable import *
from ...XCConfig.xcconfig import *
from ....Helpers import logging_helper
from ....Helpers import xcrun_helper
from ....Helpers import plist_helper

class Environment(object):
    
    def __init__(self):
        # load default environment types
        self.levels = [{}, {}, {}, {}]
        self.levels_dict = {
            'default': self.levels[0],
            'project': self.levels[1],
            'config': self.levels[2],
            'target': self.levels[3],
        };
        self.levels_lookup = ['default', 'project', 'config', 'target'];
        self.levels_order = {
            'default': 0,
            'project': 1,
            'config': 2,
            'target': 3,
        }
        
    def loadDefaults(self):
        # load spec com.apple.buildsettings.standard
        # load spec com.apple.build-system.core
        
        # setting up default environment
        self.applyConfig(xcconfig(xcconfig.pathForBuiltinConfigWithName('defaults.xcconfig')), 'default');
        self.applyConfig(xcconfig(xcconfig.pathForBuiltinConfigWithName('runtime.xcconfig')), 'default');
        xcode_version_plist_path = os.path.normpath(os.path.join(xcrun_helper.resolve_developer_path(), '../version.plist'));
        xcode_version_plist = plist_helper.LoadPlistFromDataAtPath(xcode_version_plist_path);
        xcode_version = xcode_version_plist['CFBundleShortVersionString'];
        xcode_build = xcode_version_plist['ProductBuildVersion'];
        cache_root = os.path.join(os.confstr('CS_DARWIN_USER_CACHE_DIR'), 'com.apple.DeveloperTools/'+xcode_version+'-'+xcode_build+'/Xcode');
        self.setValueForKey('CCHROOT', cache_root, {});
        self.setValueForKey('DEVELOPER_DIR', xcrun_helper.resolve_developer_path(), {});
        current_sdk = self.valueForKey('SDKROOT');
        platform_path = xcrun_helper.make_xcrun_with_args(('--show-sdk-platform-path', '--sdk', current_sdk));
        self.setValueForKey('PLATFORM_DIR', platform_path, {});
        sdk_path = xcrun_helper.resolve_sdk_path(current_sdk);
        self.setValueForKey('PLATFORM_DEVELOPER_SDK_DIR', os.path.dirname(sdk_path), {});
        
        # load these from the platform info.plist
        platform_info_path = os.path.join(platform_path, 'Info.plist');
        platform_info_plist = plist_helper.LoadPlistFromDataAtPath(platform_info_path);
        self.setValueForKey('PLATFORM_NAME', platform_info_plist['Name'], {});
        self.setValueForKey('PLATFORM_PREFERRED_ARCH', '', {});
        self.setValueForKey('PLATFORM_PRODUCT_BUILD_VERSION', '', {});
        # load defaults from platform
        for platform_default_setting_key in platform_info_plist['DefaultProperties'].keys():
            value = platform_info_plist['DefaultProperties'][platform_default_setting_key]
            self.setValueForKey(str(platform_default_setting_key), value, {});
        # load overrides
        if 'OverrideProperties' in platform_info_plist.keys():
            for platform_override_setting_key in platform_info_plist['OverrideProperties'].keys():
                value = platform_info_plist['OverrideProperties'][platform_override_setting_key];
                self.setValueForKey(str(platform_override_setting_key), value, {});
        
        # load these from sdk info.plist
        sdk_info_path = os.path.join(sdk_path, 'SDKSettings.plist');
        sdk_info_plist = plist_helper.LoadPlistFromDataAtPath(sdk_info_path);
        self.setValueForKey('SDKROOT', sdk_info_plist['CanonicalName'], {});
        self.setValueForKey('SDK_DIR', xcrun_helper.resolve_sdk_path(sdk_info_plist['CanonicalName']), {});
        self.setValueForKey('SDK_NAME', sdk_info_plist['CanonicalName'], {});
        self.setValueForKey('SDK_PRODUCT_BUILD_VERSION', '', {});
        for sdk_default_setting_key in sdk_info_plist['DefaultProperties'].keys():
            value = sdk_info_plist['DefaultProperties'][sdk_default_setting_key];
            self.setValueForKey(str(sdk_default_setting_key), value, {});
        
        self.setValueForKey('CLANG_ANALYZER_MALLOC', 'YES', {});
        self.setValueForKey('MODULE_CACHE_DIR', os.path.join(xcrun_helper.ResolveDerivedDataPath(), 'ModuleCache'), {});
    
    def addOptions(self, options_array, level_name='default'):
        for item in options_array:
            item_name = str(item['Name']);
            for current_level_name in self.levels_lookup:
                level = self.levels_dict[current_level_name];
                if level_name == current_level_name:
                    # this is the level we want to add or merge the setting properties of
                    if item_name in self.levels_dict[level_name].keys():
                        self.levels_dict[level_name][item_name].mergeDefinition(item);
                    else:
                        self.levels_dict[level_name][item_name] = EnvVariable(item);
                else:
                    # non-aggressively propogate the additional properties to the same setting on other levels
                    if item_name in level.keys():
                        level[item_name].mergeDefinition(item, False);
    
    def removeOptions(self, options_array, level_name='default'):
        for item in options_array:
            item_name = str(item['Name']);
            for current_level_name in self.levels_lookup:
                level = self.levels_dict[current_level_name];
                if level_name == current_level_name:
                    # this is the level we want to add or merge the setting properties of
                    if item_name in self.levels_dict[level_name].keys():
                        self.levels_dict[level_name][item_name].removeDefinition(item);
                    else:
                        self.levels_dict[level_name][item_name] = None;
                else:
                    # non-aggressively propogate the additional properties to the same setting on other levels
                    if item_name in level.keys():
                        level[item_name].removeDefinition(item, False);
    
    def applyConfig(self, config_obj, level_name='config'):
        for line in config_obj.lines:
            if line.type == 'KV':
                self.setValueForKey(str(line.key()), line.value(None), line.conditions(), level_name);
            if line.type == 'COMMENT':
                # ignore this type of line
                continue;
            if line.type == 'INCLUDE':
                base_path = os.path.dirname(config_obj.path);
                path = line.includePath(base_path);
                self.applyConfig(xcconfig(path));
    
    def isEnvironmentVariable(self, key_string):
        is_envar = False;
        find_sub = key_string.find('$');
        if find_sub != -1:
            offset = find_sub + 1;
            next_char = key_string[offset];
            if next_char == '(' or next_char == '{':
                is_envar = True;
        return is_envar;
    
    def __extractKey(self, key_string):
        return key_string[2:-1];

    def __findAndSubKey(self, key_name, key_string, lookup_dict):
        # finding variable keys
        iter = re.finditer(r'\$[\(|\{]\w*[\)|\}]', key_string);
        new_string = '';
        offset = 0
        for item in iter:
            # extracting the key name
            key = self.__extractKey(item.group());
            # check if the key is found
            if key in lookup_dict.keys():
                value = self.valueForKey(key, lookup_dict=lookup_dict);
                new_string += key_string[offset:item.start()] + value;
                offset = item.end();
            else:
                offset = item.end();
                if key == 'inherited':
                    resolved_value = lookup_dict[key_name].inheritedValue();
                    if resolved_value != None:
                        resolved_value = resolved_value.value(self, lookup_dict=lookup_dict);
                    else:
                        resolved_value = '';
                    new_string += key_string[offset:item.start()] + resolved_value;
                    offset = item.end();
                else:
                    logging_helper.getLogger().warn('[Environment]: Substituting empty string for "%s" in "%s"' % (key, key_string));
                    new_string += key_string[offset:item.start()] + '';
                    offset = item.end();
        new_string += key_string[offset:];
        return new_string;
    
    def parseKey(self, key, key_string, lookup_dict=None):
        if lookup_dict == None:
            lookup_dict = self.resolvedValues();
        done_key = False;
        while done_key == False:
            temp = self.__findAndSubKey(key, key_string, lookup_dict=lookup_dict);
            if temp == key_string:
                done_key = True;
            key_string = temp;
        return (True, key_string, len(key_string));
    
    def setValueForKey(self, key, value, condition_dict, level_name='default'):
        if key not in self.levels_dict[level_name].keys():
            option_dict = {};
            option_dict['Name'] = key;
            if len(condition_dict.keys()) == 0:
                option_dict['DefaultValue'] = value;
            else:
                option_dict['DefaultValue'] = '';
            self.levels_dict[level_name][key] = EnvVariable(option_dict);
        if key in self.levels_dict[level_name].keys():
            result = self.levels_dict[level_name][key];
            if result != None:
                result.addConditionalValue(EnvVarCondition(condition_dict, value));
    
    def levelForVariable(self, variable):
        for level_name in self.levels_lookup:
            level = self.levels_dict[level_name];
            if variable.name in level.keys():
                if level[variable.name] == variable:
                    return (True, level_name);
        return (False, None);
    
    def valueForKey(self, key, level_name='target', lookup_dict=None):
        value = None;
        if lookup_dict == None:
            lookup_dict = self.resolvedValues();
        if key in lookup_dict.keys():
            result = lookup_dict[key];
            if result != None:
                value = result.value(self, lookup_dict=lookup_dict);
            if value != None:
                test_value = self.parseKey(key, value, lookup_dict=lookup_dict);
                if test_value[0] == True:
                    value = test_value[1];
        return value;
    
    def getBuildComponents(self):
        components_lookup_dict = {
            'build': 'headers build',
            'analyze': 'headers build',
            'copysrc': 'source',
            'copyhdrs': 'headers',
            'copyrsrcs': 'resources',
            'install': 'headers build',
            'installdebugonly': 'build',
            'installprofileonly': 'build',
            'installdebugprofileonly': 'build',
            'installhdrs': 'headers',
            'installsrc': 'source',
            'installrsrcs': 'resources',
        };
        additional_settings_lookup_dict = {
            'installdebugonly': [('DEPLOYMENT_LOCATION', 'YES'), ('DEPLOYMENT_POSTPROCESSING', 'YES'), ('BUILD_VARIANTS', 'debug')],
            'installprofileonly': [('DEPLOYMENT_LOCATION', 'YES'), ('DEPLOYMENT_POSTPROCESSING', 'YES'), ('BUILD_VARIANTS', 'profile')],
            'installdebugprofileonly': [('DEPLOYMENT_LOCATION', 'YES'), ('DEPLOYMENT_POSTPROCESSING', 'YES'), ('BUILD_VARIANTS', 'profile debug')],
            'installhdrs': [('DEPLOYMENT_LOCATION', 'YES'), ('DEPLOYMENT_POSTPROCESSING', 'YES')],
            'installsrc': [('DEPLOYMENT_LOCATION', 'YES'), ('DEPLOYMENT_POSTPROCESSING', 'YES')],
            'installrsrcs': [('DEPLOYMENT_LOCATION', 'YES'), ('DEPLOYMENT_POSTPROCESSING', 'YES')],
        };
        action_value = self.valueForKey('ACTION');
        if action_value in additional_settings_lookup_dict.keys():
            values = additional_settings_lookup_dict[action_value];
            for value in values:
                self.setValueForKey(str(value[0]), value[1], {}, 'default');
        if action_value in components_lookup_dict.keys():
            return components_lookup_dict[action_value];
        else:
            logging_helper.getLogger().warn('[Environment]: Unable to find ACTION');
            return '';
    
    def resolvedValues(self):
        settings = {};
        for level_name in self.levels_lookup:
            level = self.levels_dict[level_name];
            for key in level.keys():
                if key in settings.keys():
                    level[key].parentValue = settings[key];
                settings[key] = level[key];
        return settings;
    
    def exportValues(self):
        export_list = [];
        key_dict = self.resolvedValues();
        for key in sorted(key_dict.keys()):
            #if key_dict[key].added_after == False:
                value = self.valueForKey(key, lookup_dict=key_dict);
                if key == 'SDKROOT':
                    result = (True, xcrun_helper.resolve_sdk_path(value), 0);
                else:
                    result = self.parseKey(key, value, lookup_dict=key_dict);
                if result[0] == True:
                    value = result[1];
                export_item = 'export '+key+'=';
                if key_dict[key].isString():
                    export_item += '"'+value+'"';
                else:
                    export_item += value;
                export_list.append(export_item);
        return export_list;