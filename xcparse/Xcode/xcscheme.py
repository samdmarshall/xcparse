import os
import sys
import xml.etree.ElementTree as xml

from ..Helpers import path_helper
from ..Helpers import xcrun_helper
from ..Helpers import logging_helper

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
                else:
                    logging_helper.getLogger().warn('[xcscheme]: Invalid scheme file at path "%s"' % scheme_file_path);
            else:
                logging_helper.getLogger().warn('[xcscheme]: "%s" is not an xcscheme file!' % scheme_file_path);
    else:
        logging_helper.getLogger().warn('[xcscheme]: "%s" path does not exist!' % dir_path);
    return schemes;

class xcscheme(object):
    
    def __init__(self, path):
        self.shared = False;
        self.container = '';
        self.path = path_helper(path, '');
        self.name = os.path.basename(path).split('.xcscheme')[0];
        self.contents = None;
        try:
            self.contents = xml.parse(self.path.obj_path);
        except:
            logging_helper.getLogger().error('[xcscheme]: Could not load contents of xcscheme file!');
    
    def __repr__(self):
        if self.isValid():
            return '(%s : %s : %s)' % (type(self), self.name, self.path);
        else:
            return '(%s : INVALID OBJECT)' % (type(self));
    
    def __attrs(self):
        return (self.name, self.path);

    def __eq__(self, other):
        return isinstance(other, xcscheme) and self.name == other.name and self.path.root_path == other.path.root_path;

    def __hash__(self):
        return hash(self.__attrs());
    
    def actionLookup(self, action_name):
        """
        This method returns the method for the passed action type, None otherwise.
        """
        action_name = action_name.lower();
        lookup = {
            'build': self.buildAction,
            'test': self.testAction,
            'launch': self.launchAction,
            'profile': self.profileAction,
            'analyze': self.analyzeAction,
            'archive': self.archiveAction
        };
        action = None;
        if action_name in lookup.keys():
            action = lookup[action_name];
        return action;
    
    def isValid(self):
        return self.contents != None;
    
    def getAction(self, action_type):
        """
        This method returns all the object for the passed action type, otherwise None.
        """
        action = None;
        if self.isValid():
            action = filter(lambda action: action.tag == action_type, list(self.contents.getroot()))[0];
        return action;
    
    def buildAction(self, container):
        """
        Returns the 'build' action for this scheme.
        """
        action = None;
        if self.isValid():
            action = BuildAction(self.getAction('BuildAction'));
        return action;
    
    def testAction(self, container):
        """
        Returns the 'test' action for this scheme.
        """
        action = None;
        if self.isValid():
            action = TestAction(self.getAction('TestAction'));
            action.root = BuildAction(self.getAction('BuildAction'))
        return action;
    
    def launchAction(self, container):
        """
        Returns the 'launch' action for this scheme.
        """
        action = None;
        if self.isValid():
            action = LaunchAction(self.getAction('LaunchAction'));
        return action;
    
    def profileAction(self, container):
        """
        Returns the 'profile' action for this scheme.
        """
        action = None;
        if self.isValid():
            action = ProfileAction(self.getAction('ProfileAction'));
        return action;
    
    def analyzeAction(self, container):
        """
        Returns the 'analyze' action for this scheme.
        """
        action = None;
        if self.isValid():
            action = AnalyzeAction(self.getAction('AnalyzeAction'));
            action.root = BuildAction(self.getAction('BuildAction'))
        return action;
    
    def archiveAction(self, container):
        """
        Returns the 'archive' action for this scheme.
        """
        action = None;
        if self.isValid():
            action = ArchiveAction(self.getAction('ArchiveAction'));
            action.root = BuildAction(self.getAction('BuildAction'))
        return action;
    