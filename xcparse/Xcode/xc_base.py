from PBX import PBXResolver
from .xcscheme import *

class xc_base(object):
    
    def __init__(self, path):
        self.path = path;
    
    def schemes(self):
        """
        This method is used for both 'xcworkspace' and 'xcodeproj' classes. It returns a
        list of schemes that are labeled as 'user' or 'shared'.
        """
        schemes = [];
        # shared schemes
        shared_path = XCSchemeGetSharedPath(self.path.obj_path);
        shared_schemes = XCSchemeParseDirectory(shared_path);
        for scheme in shared_schemes:
            scheme.shared = True;
        # user schemes
        user_path = XCSchemeGetUserPath(self.path.obj_path);
        user_schemes = XCSchemeParseDirectory(user_path);
        # merge schemes
        for scheme in shared_schemes + user_schemes:
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
        result = scheme_name in list(map(lambda scheme: scheme.name, schemes));
        found_scheme = None;
        for scheme in schemes:
            if scheme.name == scheme_name:
                found_scheme = scheme;
                break;
        return (result, found_scheme);