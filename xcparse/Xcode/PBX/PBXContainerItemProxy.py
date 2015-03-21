from .PBX_Base import *

class PBXContainerItemProxy(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        super(PBXContainerItemProxy, self).__init__(lookup_func, dictionary, project, identifier);
        if 'containerPortal' in dictionary.keys():
            self.containerPortal = dictionary['containerPortal'];
        if 'proxyType' in dictionary.keys():
            self.proxyType = dictionary['proxyType'];
        if 'remoteGlobalIDString' in dictionary.keys():
            self.remoteGlobalIDString = dictionary['remoteGlobalIDString'];
        if 'remoteInfo' in dictionary.keys():
            self.remoteInfo = dictionary['remoteInfo'];