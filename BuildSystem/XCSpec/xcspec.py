from .spec_base import *

class xcspec(spec_base):
    
    def inheritedTypes(self):
        types = [str(self.identifier)];
        if self.basedOn != None:
            parent = self.basedOn.inheritedTypes();
            types.extend(parent);
        return types;