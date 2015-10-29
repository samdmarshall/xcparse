# import Cocoa
# import Foundation
import pbPlist
import os
import sys
import logging_helper

class plist_helper(object):
    @classmethod
    def LoadPlistFromDataAtPath(cls, path):
        contents = None;
        if os.path.exists(path) == True:
            try:
                result = pbPlist.PBPlist(path);
                contents = result.root
                # if result.file_type == 'ascii':
                #     contents = result.root.value
                # else:
                #     contents = result.root
            except:
                raise
        else:
            logging_helper.getLogger().error('[plist_helper]: path doesn\'t exist!');
        return contents;

    @classmethod
    def LoadPlistFromStringAtPath(cls, path):
        contents = None;
        if os.path.exists(path) == True:
            # loading spec file
            try:
                result = pbPlist.PBPlist(path);
                if result.file_type == 'ascii':
                    contents = result.root.value
                else:
                    contents = result.root
            except:
                raise
        else:
            logging_helper.getLogger().error('[plist_helper]: Path does not exist!');
        return contents;