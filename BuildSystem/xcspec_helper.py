import Cocoa
import Foundation

from ..Path import *
from ..xcrun import *

from .XCSpec.xcspec import *
from .XCSpec.xcspec_resolver import *

def xcspecLoadFileAtRelativeDeveloperPath(path):
    xcspec_path = os.path.normpath(os.path.join(xcrun.resolve_developer_path(), path));
    if os.path.exists(xcspec_path) == True:
        return xcspecLoadFromContentsAtPath(xcspec_path);
    else:
        return [];

def xcspecLoadFromContentsAtPath(spec_path):
    contents = None;
    if spec_path.endswith('spec'):
        path = Path(spec_path, '');
        
        if os.path.exists(path.root_path) == True:
            # loading spec file
            specNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(path.root_path, Foundation.NSUncachedRead, None);
            if errorMessage == None:
                specString = Foundation.NSString.alloc().initWithData_encoding_(specNSData, Foundation.NSUTF8StringEncoding);
                if specString != None:
                    contents = specString.propertyList();
                else:
                    print 'Could not load string from data';
            else:
                print errorMessage;
        else:
            print 'Path does not exist!';
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