from PBX import PBXResolver
from .xcscheme import *
from ..Helpers import path_helper
from ..Helpers import logging_helper

class xc_base(object):
    
    def __init__(self, path):
        self.path = path;
        self.identifier = path_helper(path, '');
        self.contents = None;
    
    def __repr__(self):
        if self.isValid():
            return '(%s : %s : %s)' % (type(self), self.path, self.identifier);
        else:
            return '(%s : INVALID OBJECT)' % (type(self));
    
    def __attrs(self):
        return (self.identifier, self.path);

    def __eq__(self, other):
        return isinstance(other, xcodeproj) and self.identifier == other.identifier and self.path.root_path == other.path.root_path;

    def __hash__(self):
        return hash(self.__attrs());
    
    def isValid(self):
        return self.contents != None;
    
    def schemes(self):
        """
        This method is used for both 'xcworkspace' and 'xcodeproj' classes. It returns a
        list of schemes that are labeled as 'user' or 'shared'.
        """
        schemes = [];
        # shared schemes
        if XCSchemeHasSharedSchemes(self.path.obj_path) == True:
            shared_path = XCSchemeGetSharedPath(self.path.obj_path);
            shared_schemes = XCSchemeParseDirectory(shared_path);
            for scheme in shared_schemes:
                scheme.shared = True;
                scheme.container = self.path;
                schemes.append(scheme);
        # user schemes
        if XCSchemeHasUserSchemes(self.path.obj_path) == True:
            user_path = XCSchemeGetUserPath(self.path.obj_path);
            user_schemes = XCSchemeParseDirectory(user_path);
            for scheme in user_schemes:
                scheme.container = self.path;
                schemes.append(scheme);
        return schemes;
    
    def hasSchemeWithName(self, scheme_name):
        """
        This method is used for both 'xcworkspace' and 'xcodeproj' classes. It returns a two
        element tuple that contains the following:
        
        First element:
            A 'True' or 'False' value indicating if a scheme with the passed name was found in 
            this project or workspace file.
        
        Second element:
            The scheme object if a scheme with matching name was found, None otherwise.
        """
        schemes = self.schemes();
        found_scheme = None;
        scheme_filter = filter(lambda scheme: scheme.name == scheme_name, schemes);
        if len(scheme_filter) > 0:
            found_scheme = scheme_filter[0];
        return (found_scheme != None, found_scheme);
    
    def projects(self):
        logging_helper.getLogger().error('[xc_base]: DO NOT CALL THIS METHOD DIRECTLY, SUBCLASS THIS OBJECT TO IMPLEMENT!');
        return [];