from ...Helpers import xcrun_helper

class xcbuildrule(object):
    
    def __init__(self, rule_dictionary):
        self.name = rule_dictionary['Name'];
        self.identifier = rule_dictionary['CompilerSpec'];
        self.fileTypes = rule_dictionary['FileType'];
    
    def __attrs(self):
        return (self.identifier);
    
    def __repr__(self):
        return '(%s : %s : %s)' % (type(self), self.name, self.identifier);
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.identifier == other.identifier;
    
    def __hash__(self):
        return hash(self.__attrs());