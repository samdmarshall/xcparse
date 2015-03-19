from .PBXResolver import *

class PBX_Base(object):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.name = 'PBX_BASE';
        self.identifier = identifier;
    
    def __attrs(self):
        return (self.identifier);
    
    def __repr__(self):
        return '(%s : %s : %s)' % (type(self), self.name, self.identifier);
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.identifier == other.identifier;
    
    def __hash__(self):
        return hash(self.__attrs());
    
    def resolve(self, type, list):
        return filter(lambda item: isinstance(item, type), list);
    
    def parseProperty(self, prop_name, lookup_func, dictionary, project, is_array):
        dict_item = dictionary[prop_name];
        if is_array == True:
            property_list = [];
            for item in dict_item:
                find_object = project.objectForIdentifier(item);
                if find_object != None:
                    property_list.append(find_object);
                else:
                    result = lookup_func(project.contents['objects'][item]);
                    if result[0] == True:
                        created_object = result[1](lookup_func, project.contents['objects'][item], project, item);
                        project.objects.add(created_object);
                        property_list.append(created_object);
            return property_list;
        else:
            property_item = None;
            find_object = project.objectForIdentifier(dict_item);
            if find_object != None:
                property_item = find_object;
            else:
                result = lookup_func(project.contents['objects'][dict_item])
                if result[0] == True:
                    property_item = result[1](lookup_func, project.contents['objects'][dict_item], project, dict_item);
                    project.objects.add(property_item);
            return property_item;
    