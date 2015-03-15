class xcconfig_item_base(object):
    
    def __init__(self, line):
        line_end = line.find('//');
        if line_end > 0:
            line = line[:line_end];
        self.contents = line;
        self.type = 'EMPTY';
    
    def __repr__(self):
        if self.isValid():
            return '(%s : %s : %s)' % (type(self), self.type, self.contents);
        else:
            return '(%s : IGNORED LINE)' % (type(self));
    
    def __attrs(self):
        return (self.type, self.contents);

    def __eq__(self, other):
        return isinstance(other, xcconfig_item_base) and self.type == other.type and self.contents == other.contents;

    def __hash__(self):
        return hash(self.__attrs());
    
    def isValid(self):
        return self.type != 'EMPTY';
    