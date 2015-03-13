import sys
import argparse
import xcparse

def main(argv):
    parser = argparse.ArgumentParser(description='Test xcparse');
    parser.add_argument('filename', help='path to xcodeproj or xcworkspace');
    args = parser.parse_args();
    
    result = xcparse.xcparse(args.filename);
    
    print result;
    

if __name__ == "__main__":
    main(sys.argv[1:]);