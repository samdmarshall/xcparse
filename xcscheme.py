from __future__ import absolute_import
import os
import sys
import xml.etree.ElementTree as xml

from .Path import *

from .xcrun import *

from .XCSchemeActions.BuildAction import BuildAction
from .XCSchemeActions.TestAction import TestAction
from .XCSchemeActions.LaunchAction import LaunchAction
from .XCSchemeActions.ProfileAction import ProfileAction
from .XCSchemeActions.AnalyzeAction import AnalyzeAction
from .XCSchemeActions.ArchiveAction import ArchiveAction

def XCSchemeGetSharedPath(path):
    return os.path.join(path, 'xcshareddata/xcschemes');

def XCSchemeGetUserPath(path):
    return os.path.join(path, 'xcuserdata/'+os.getlogin()+'.xcuserdatad/xcschemes/');

def XCSchemeParseDirectory(dir_path):
    schemes = [];
    if os.path.exists(dir_path) == True:
        for scheme_file in os.listdir(dir_path):
            scheme_file_path = os.path.join(dir_path, scheme_file);
            if not scheme_file.startswith('.') and scheme_file_path.endswith('.xcscheme') and os.path.isfile(scheme_file_path):
                scheme_xml = xcscheme(scheme_file_path);
                if scheme_xml.isValid() == True:
                    schemes.append(scheme_xml);
    return schemes;

def XCSchemeName(x):
    return x.name;

class xcscheme(object):
    # path = {};
    # contents = {};
    # name = '';
    
    def __init__(self, path):
        self.shared = False;
        self.container = '';
        self.path = Path(path, '');
        self.name = os.path.basename(path).split('.xcscheme')[0];
        try:
            self.contents = xml.parse(self.path.obj_path);
        except:
            self.contents = None;
    
    def actionLookup(self, action_name):
        action_name = action_name.lower();
        lookup = {
            'build': self.buildAction,
            'test': self.testAction,
            'launch': self.launchAction,
            'profile': self.profileAction,
            'analyze': self.analyzeAction,
            'archive': self.archiveAction
        };
        if action_name in lookup.keys():
            return lookup[action_name];
        else:
            return None;
    
    def isValid(self):
        return self.contents != None;
    
    def getAction(self, action_type):
        if self.isValid():
            return filter(lambda action: action.tag == action_type, list(self.contents.getroot()))[0];
        else:
            return None;
    
    def buildAction(self, container):
        if self.isValid():
            action = BuildAction(self.getAction('BuildAction'));
            return action;
        else:
            return None;
    
    def testAction(self, container):
        if self.isValid():
            action = TestAction(self.getAction('TestAction'));
            action.root = BuildAction(self.getAction('BuildAction'))
            return action;
        else:
            return None;
    
    def launchAction(self, container):
        if self.isValid():
            action = LaunchAction(self.getAction('LaunchAction'));
            return action;
        else:
            return None;
    
    def profileAction(self, container):
        if self.isValid():
            action = ProfileAction(self.getAction('ProfileAction'));
            return action;
        else:
            return None;
    
    def analyzeAction(self, container):
        if self.isValid():
            action = AnalyzeAction(self.getAction('AnalyzeAction'));
            action.root = BuildAction(self.getAction('BuildAction'))
            return action;
        else:
            return None;
    
    def archiveAction(self, container):
        if self.isValid():
            action = ArchiveAction(self.getAction('ArchiveAction'));
            action.root = BuildAction(self.getAction('BuildAction'))
            return action;
        else:
            return None;