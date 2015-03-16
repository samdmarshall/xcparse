class EnvVarCondition(object):
    
    # this object needs to hash so that we don't get duplicate conditional cases
    
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