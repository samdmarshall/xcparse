from ...Helpers import xcrun_helper

class xcbuildrule(object):
    
    def __init__(self, spec):
        self.name = spec.name;
        self.identifier = spec.identifier;
        self.fileTypes = [];
        if 'FileTypes' in spec.contents:
            self.fileTypes = spec.contents['FileTypes'];
        if 'SynthesizeBuildRule' in spec.contents:
            if spec.contents['SynthesizeBuildRule'] == 'YES':
                self.fileTypes = spec.contents['InputFileTypes'];
    
    def __attrs(self):
        return (self.identifier);
    
    def __repr__(self):
        return '%s : %s : %s' % (type(self), self.name, self.identifier);
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.identifier == other.identifier;
    
    def __hash__(self):
        return hash(self.__attrs());