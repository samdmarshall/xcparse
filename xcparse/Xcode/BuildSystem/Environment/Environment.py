import os
from .EnvVarCondition import *
from .EnvVariable import *
from ...XCConfig.xcconfig import *
from ....Helpers import logging_helper
from ....Helpers import xcrun_helper
from ....Helpers import plist_helper

class Environment(object):
    
    def __init__(self):
        self.settings = {};
        # load default environment types
        
    def loadDefaults(self):
        # setting up default environment
        self.applyConfig(xcconfig(xcconfig.pathForBuiltinConfigWithName('defaults.xcconfig')));
        self.applyConfig(xcconfig(xcconfig.pathForBuiltinConfigWithName('runtime.xcconfig')));
        platform_path = xcrun_helper.make_xcrun_with_args(('--show-sdk-platform-path', '--sdk', self.valueForKey('SDKROOT')));
        self.setValueForKey('PLATFORM_DIR', platform_path, {});
        sdk_path = xcrun_helper.resolve_sdk_path(self.valueForKey('SDKROOT'));
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
            self.setValueForKey(platform_default_setting_key, value, {});
        # load overrides
        if 'OverrideProperties' in platform_info_plist.keys():
            for platform_override_setting_key in platform_info_plist['OverrideProperties'].keys():
                value = platform_info_plist['OverrideProperties'][platform_override_setting_key];
                self.setValueForKey(platform_override_setting_key, value, {});
        
        # load these from sdk info.plist
        sdk_info_path = os.path.join(sdk_path, 'SDKSettings.plist');
        sdk_info_plist = plist_helper.LoadPlistFromDataAtPath(sdk_info_path);
        self.setValueForKey('SDKROOT', sdk_info_plist['CanonicalName'], {});
        for sdk_default_setting_key in sdk_info_plist['DefaultProperties'].keys():
            value = sdk_info_plist['DefaultProperties'][sdk_default_setting_key];
            self.setValueForKey(sdk_default_setting_key, value, {});
        
    
    def addOptions(self, options_array):
        for item in options_array:
            if item['Name'] in self.settings.keys():
                print 'over-write key %s' % item['Name'];
                #print item;
            else:
                self.settings[item['Name']] = EnvVariable(item);
    
    def applyConfig(self, config_obj):
        for line in config_obj.lines:
            if line.type == 'KV':
                self.setValueForKey(line.key(), line.value(None), line.conditions());
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
    
    def parseKey(self, key_string):
        key = '';
        value = '';
        string_length = len(key_string);
        offset = 0;
        key_length = 0;
        find_sub = key_string.find('$');
        if find_sub != -1:
            start = find_sub;
            end = 0;
            offset = find_sub + 1;
            next_char = key_string[offset];
            if next_char == '(' or next_char == '{':
                offset += 1;
                while offset < string_length:
                    if key_string[offset] == '$':
                        subkey = key_string[offset:];
                        print 'found subkey "%s"' % subkey;
                        sub_value = self.parseKey(subkey);
                        if sub_value[0] == False:
                            logging_helper.getLogger().error('[Environment]: Error in parsing key "%s"' % key_string);
                        append_value = '';
                        if sub_value[1] != None:
                            append_value = sub_value[1];
                        key += append_value;
                        offset += sub_value[2];
                    elif key_string[offset] == ')' or key_string[offset] == '}':
                        end = offset;
                        break;
                    else:
                        key += key_string[offset];
                    offset += 1;
                value = self.valueForKey(key);
                key_length = end - start;
        # the key has to contain a subtitutable value, and the value cannot be None
        return (key_length != 0 and value != None, value, key_length);
    
    def setValueForKey(self, key, value, condition_dict):
        if key not in self.settings.keys():
            option_dict = {};
            option_dict['Name'] = key;
            if len(condition_dict.keys()) == 0:
                option_dict['DefaultValue'] = value;
            else:
                option_dict['DefaultValue'] = '';
            self.settings[key] = EnvVariable(option_dict);
        if key in self.settings.keys():
            result = self.settings[key];
            if result != None:
                result.addConditionalValue(EnvVarCondition(condition_dict, value));
        
    
    def valueForKey(self, key):
        value = None;
        if key in self.settings.keys():
            result = self.settings[key];
            if result != None:
                value = result.value(self);
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
                self.setValueForKey(value[0], value[1], {});
        if action_value in components_lookup_dict.keys():
            return components_lookup_dict[action_value];
        else:
            logging_helper.getLogger().warn('[Environment]: Unable to find ACTION');
            return '';
    
    
    def exportValues(self):
        export_list = [];
        for key in sorted(self.settings.keys()):
            # this need to change to parse out the resulting values completely
            value = self.valueForKey(key);
            result = self.parseKey(value);
            if result[0] == True:
                value = result[1];
            export_item = 'export '+key+'=';
            if self.settings[key].type == 'String':
                export_item += '"'+value+'"';
            else:
                export_item += value;
            export_list.append(export_item);
        return export_list;