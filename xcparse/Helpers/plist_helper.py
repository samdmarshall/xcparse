import Cocoa
import Foundation
import os
import logging_helper

class plist_helper(object):
    @classmethod
    def LoadPlistFromDataAtPath(cls, path):
        contents = None;
        if os.path.exists(path) == True:
            plistNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(path, Foundation.NSUncachedRead, None);
            if errorMessage == None:
                plistContents, plistFormat, errorMessage = Foundation.NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(plistNSData, Foundation.NSPropertyListMutableContainers, None, None);
                if errorMessage == None:
                    contents = plistContents;
                else:
                    logging_helper.getLogger().error('[plist_helper]: %s' % errorMessage);
            else:
                logging_helper.getLogger().error('[plist_helper]: %s' % errorMessage);
        else:
            logging_helper.getLogger().error('[plist_helper]: path doesn\'t exist!');
        return contents;

    @classmethod
    def LoadPlistFromStringAtPath(cls, path):
        contents = None;
        if os.path.exists(path) == True:
            # loading spec file
            specNSData, errorMessage = Foundation.NSData.dataWithContentsOfFile_options_error_(path, Foundation.NSUncachedRead, None);
            if errorMessage == None:
                specString = Foundation.NSString.alloc().initWithData_encoding_(specNSData, Foundation.NSUTF8StringEncoding);
                if specString != None:
                    contents = specString.propertyList();
                else:
                    logging_helper.getLogger().error('[plist_helper]: Could not load string from data');
            else:
                logging_helper.getLogger().error('[plist_helper]: %s' % errorMessage);
        else:
            logging_helper.getLogger().error('[plist_helper]: Path does not exist!');
        return contents;