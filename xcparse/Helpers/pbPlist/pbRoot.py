import collections

import pbItem

class pbRoot(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.key_storage = set()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __internalKeyCheck(self, key):
        safe_key = key
        if type(safe_key) == str:
            safe_key = pbItem.pbItemResolver(safe_key, 'qstring')
        return safe_key

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key not in self.key_storage:
            self.key_storage.add(self.__internalKeyCheck(key))
        self.store[key] = value

    def __delitem__(self, key):
        if key in self.key_storage:
            self.key_storage.remove(key)
        del self.store[key]

    def __iter__(self):
        return self.key_storage.__iter__()

    def __len__(self):
        return self.key_storage.__len__()
    
    def __str__(self):
        return self.store.__str__()
    
    def __contains__(self, item):
        return item in self.key_storage
    
    def __getattr__(self, attrib):
        return getattr(self.store, attrib)

    def __keytransform__(self, key):
        if isinstance(key, pbItem.pbItem):
            return key.value
        else:
            return key