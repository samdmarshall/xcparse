import sys
import os
import argparse
import xcparse
from xcparse.Xcode.PBX.PBXGroup import PBXGroup

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path);

def make_file(path, item):
    if not os.path.exists(path):
        file = open(path, 'w+');
        file.write(item.identifier);
        file.write('\n\r');
        file.write('#'+item.name+'\n\r');
        file.close();

def print_name(item, depth):
    tree_string = '|';
    if depth > 0:
        total = depth+(depth*3);
        tree_string += '%*s|' % (total, ' '*(total))
    tree_string += '-- ' + item.name;
    print tree_string;

def create_docs(item, docs_path):
    filename = item.name+'.md';
    make_file(docs_path+'.md', item);
    if isinstance(item, PBXGroup):
        make_dir(docs_path);

def print_level(item_array, depth, docs_path):
    for item in item_array:
        print_name(item, depth);
        item_doc_path = os.path.join(docs_path, item.name);
        create_docs(item, item_doc_path);
        if isinstance(item, PBXGroup):
            print_level(item.children, depth+1, item_doc_path);

def file_structure_docs(proj, project_root_path):
    docs_path = os.path.join(project_root_path, 'ProjectDocs');
    make_dir(docs_path);
    top_level_groups = filter(lambda item: item.identifier != proj.rootObject.productRefGroup, proj.rootObject.mainGroup.children)
    print_level(top_level_groups, 0, docs_path);

def main(argv):
    parser = argparse.ArgumentParser(description='Build documentation for Xcode Project file');
    parser.add_argument('filename', help='path to xcodeproj or xcworkspace');
    args = parser.parse_args();
    
    xcparser = xcparse.xcparse(args.filename);
    
    project_root = os.path.dirname(args.filename);
    for proj in xcparser.projects():
        print '====='+os.path.basename(proj.path.obj_path)+'=====';
        file_structure_docs(proj, project_root);

if __name__ == "__main__":
    main(sys.argv[1:]);