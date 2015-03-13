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
    if spec_path.endswith('spec'):
        path = path_helper(spec_path, '');
        
        contents = plist_helper.LoadPlistFromStringAtPath(path.root_path);
    else:
        print 'Not a xcspec file!';
    
    items = [];
    
    if contents != None:
        if hasattr(contents, 'keys'):
            constructor = xcspec_resolver(contents);
            if constructor[0] == True:
                items.append(constructor[1](contents));
        else:
            for spec_item in contents:
                constructor = xcspec_resolver(spec_item);
                if constructor[0] == True:
                    items.append(constructor[1](spec_item));
    
    return items;