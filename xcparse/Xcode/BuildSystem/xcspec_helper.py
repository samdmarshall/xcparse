from ...Helpers import logging_helper
from ...Helpers import plist_helper
from ...Helpers import path_helper
from ...Helpers import xcrun_helper

from .XCSpec.xcspec import *
from .XCSpec.xcspec_resolver import *

def xcspecLoadFileAtRelativeDeveloperPath(path):
    xcspec_path = os.path.normpath(os.path.join(xcrun_helper.resolve_developer_path(), path));
    if os.path.exists(xcspec_path) == True:
        return xcspecLoadFromContentsAtPath(xcspec_path);
    else:
        return [];

def xcspecLoadFromContentsAtPath(spec_path):
    contents = None;
    items = [];
    if spec_path.endswith('spec'):
        path = path_helper(spec_path, '');
        
        try:
            contents = plist_helper.LoadPlistFromStringAtPath(path.root_path);
        except:
            print('Error in loading spec at path "%s"' % path.root_path)
            raise
    else:
        logging_helper.getLogger().error('[xcspec_helper]: Not a spec file!');
        return items;
    
    if contents != None:
        if hasattr(contents, 'keys'):
            if spec_path.endswith('pbfilespec') and 'Type' not in contents.keys():
                contents['Type'] = 'FileType';
            constructor = xcspec_resolver(contents);
            if constructor[0] == True:
                items.append(constructor[1](contents));
            else:
                logging_helper.getLogger().warn('[xcspec_helper]: Tried to load spec file at "%s" but couldn\'t resolve type' % spec_path);
        else:
            for spec_item in contents:
                if spec_path.endswith('pbfilespec') and 'Type' not in spec_item.keys():
                    spec_item['Type'] = 'FileType';
                constructor = xcspec_resolver(spec_item);
                if constructor[0] == True:
                    items.append(constructor[1](spec_item));
                else:
                    logging_helper.getLogger().warn('[xcspec_helper]: Tried to load spec file at "%s" but couldn\'t resolve type' % spec_path);
            if len(contents) == 0:
                logging_helper.getLogger().warn('[xcspec_helper]: No specs loaded from file at "%s"' % spec_path); 
    
    return items;