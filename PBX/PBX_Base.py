from __future__ import absolute_import
import Cocoa
import Foundation
import os

from .PBXResolver import *

class PBX_Base(object):
    
    def __init__(self, lookup_func, dictionary, project):
        self.name = 'PBX_BASE';
        
    def resolve(self, type, list):
        return filter(lambda item: isinstance(item, type), list);
    
    def parseProperty(self, prop_name, lookup_func, dictionary, project, is_array):
        dict_item = dictionary[prop_name];
        if is_array == True:
            property_list = [];
            for item in dict_item:
                result = lookup_func(project.objects()[item]);
                if result[0] == True:
                    property_list.append(result[1](lookup_func, project.objects()[item], project));
            return property_list;
        else:
            property_item = None;
            result = lookup_func(project.objects()[dict_item])
            if result[0] == True:
                property_item = result[1](lookup_func, project.objects()[dict_item], project);
            return property_item;