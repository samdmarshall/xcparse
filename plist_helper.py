import Cocoa
import Foundation
import os

def LoadPlistFromDataAtPath(path):
    contents = None;
    if os.path.exists(path) == True:
        plistNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(path, Foundation.NSUncachedRead, None);
        if errorMessage == None:
            plistContents, plistFormat, errorMessage = Foundation.NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(plistNSData, Foundation.NSPropertyListMutableContainers, None, None);
            if errorMessage == None:
                contents = plistContents;
            else:
                print errorMessage;
        else:
            print errorMessage;
    else:
        print 'path doesn\'t exist!';
    return contents;

def LoadPlistFromStringAtPath(path):
    contents = None;
    if os.path.exists(path) == True:
        # loading spec file
        specNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(path, Foundation.NSUncachedRead, None);
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
    return contents;