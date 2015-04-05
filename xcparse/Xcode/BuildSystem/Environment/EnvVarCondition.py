import re
from ....Helpers import logging_helper

class EnvVarCondition(object):
    
    def __init__(self, condition_dict, value):
        self.keys = condition_dict.keys();
        self.eval = condition_dict;
        self.value = value;
    
    def evaluate(self, environment, lookup_dict=None):
        if lookup_dict == None:
            lookup_dict = environment.resolvedValues();
        
        conditional_key_lookup_dict = {
            'sdk': 'SDKROOT',
            'variant': 'BUILD_VARIANT',
            'arch': 'ARCH',
            'config': 'CONFIGURATION',
        };
        eval_result = True;
        for key in self.keys:
            value = self.eval[key];
            # resolve the conditional
            if key in conditional_key_lookup_dict.keys():
                key = conditional_key_lookup_dict[key];
            else:
                logging_helper.getLogger().error('[EnvVarCondition]: Invalid conditional key!');
                eval_result = False;
                break;
            # lookup the conditional
            lookup_value = environment.valueForKey(key, lookup_dict=lookup_dict);
            # some check here
            value_compare = re.compile(value);
            result = value_compare.match(lookup_value);
            if result == None:
                eval_result = False;
                break;
        return eval_result;
    
    def __repr__(self):
        return '(%s : %s : %s)' % (type(self), self.eval, self.value);
    
    def __attrs(self):
        return tuple(self.keys) + tuple(self.eval.values());

    def __eq__(self, other):
        return isinstance(other, EnvVarCondition) and self.keys == other.keys;

    def __hash__(self):
        return hash(self.__attrs());
        