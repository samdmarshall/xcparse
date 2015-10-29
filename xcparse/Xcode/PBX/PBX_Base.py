from .PBXResolver import *
from .PBX_Constants import *

class PBX_Base(object):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        # default 'name' property of a PBX object is the type 
        self.name = self.__class__.__name__;
        # this is the identifier for this object
        self.identifier = str(identifier);
        # set of any referenced identifiers on this object
        self.referencedIdentifiers = set();
    
    def __attrs(self):
        return (self.identifier);
    
    def __repr__(self):
        return '(%s : %s : %s)' % (type(self), self.name, self.identifier);
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.identifier == other.identifier;
    
    def __hash__(self):
        return hash(self.__attrs());
    
    def resolve(self, type, item_list):
        return filter(lambda item: isinstance(item, type), item_list);
    
    def fetchObjectFromProject(self, lookup_func, identifier, project):
        find_object = project.objectForIdentifier(identifier);
        if find_object == None:
            result = lookup_func(project.contents[kPBX_objects][identifier]);
            if result[0] == True:
                find_object = result[1](lookup_func, project.contents[kPBX_objects][identifier], project, identifier);
                project.objects.add(find_object);
        return find_object;
    
    def parseProperty(self, prop_name, lookup_func, dictionary, project, is_array):
        dict_item = dictionary[prop_name];
        if is_array == True:
            property_list = [];
            for item in dict_item:
                self.referencedIdentifiers.add(item);
                find_object = self.fetchObjectFromProject(lookup_func, item, project);
                property_list.append(find_object);
            return property_list;
        else:
            self.referencedIdentifiers.add(dict_item);
            return self.fetchObjectFromProject(lookup_func, dict_item, project);
    