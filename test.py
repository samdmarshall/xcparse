import sys
import os
import argparse
import xcparse
from xcparse.Xcode.BuildSystem import xcbuildsystem
from xcparse.Xcode.BuildSystem.Environment import Environment
from xcparse.Xcode.XCConfig import xcconfig

def main(argv):
    parser = argparse.ArgumentParser(description='Test xcparse');
    parser.add_argument('filename', help='path to xcodeproj or xcworkspace');
    args = parser.parse_args();
    
    xcparser = xcparse.xcparse(args.filename);
    
    print xcparser.projects();

    environment = Environment();

    test_config = xcconfig(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test/test.xcconfig'));

    environment.applyConfig(test_config);

    for scheme in xcparser.schemes():
        result = xcparser.findSchemeWithName(scheme.name)[0];
        if result[0] == True:
            action_func = result[1].actionLookup('build');
            if action_func != None:
                action_item = action_func(result[2]);
                action_item.performAction(result, xcparser, 'Debug', {});

if __name__ == "__main__":
    main(sys.argv[1:]);