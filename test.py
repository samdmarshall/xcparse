import sys
import argparse
import xcparse
from xcparse.Xcode.BuildSystem import xcbuildsystem

def main(argv):
    parser = argparse.ArgumentParser(description='Test xcparse');
    parser.add_argument('filename', help='path to xcodeproj or xcworkspace');
    args = parser.parse_args();
    
    xcparser = xcparse.xcparse(args.filename);
    
    build_system = xcbuildsystem();
    
    for scheme in xcparser.schemes():
        result = xcparser.findSchemeWithName(scheme.name)[0];
        if result[0] == True:
            action_func = result[1].actionLookup('build');
            if action_func != None:
                action_item = action_func(result[2]);
                action_item.performAction(build_system, result, xcparser, {});
    
    

if __name__ == "__main__":
    main(sys.argv[1:]);