class EnvVarCondition(object):
    
    def __init__(self, condition_dict, value):
        self.keys = condition_dict.keys();
        self.eval = condition_dict;
        self.value = value;
    
    def evaluate(self, environment):
        for key in self.keys():
            # lookup the conditional
            result = environment.valueForKey(key);
            # some check here
            print result;
            # break if failed
        return False;
    
    def __repr__(self):
        return '(%s : %s : %s)' % (type(self), self.eval, self.value);
    
    def __attrs(self):
        return tuple(self.keys);

    def __eq__(self, other):
        return isinstance(other, EnvVarCondition) and self.keys == other.keys;

    def __hash__(self):
        return hash(self.__attrs())