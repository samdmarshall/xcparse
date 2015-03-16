from .PBXResolver import *
from .PBX_Base import *

class XCConfigurationList(PBX_Base):
    
    def __init__(self, lookup_func, dictionary, project, identifier):
        self.identifier = identifier;
        self.defaultConfigurationName = None;
        if 'buildConfigurations' in dictionary.keys():
            self.buildConfigurations = self.parseProperty('buildConfigurations', lookup_func, dictionary, project, True);
        if 'defaultConfigurationName' in dictionary.keys():
            self.defaultConfigurationName = dictionary['defaultConfigurationName'];
        if 'defaultConfigurationIsVisible' in dictionary.keys():
            self.defaultConfigurationIsVisible = dictionary['defaultConfigurationIsVisible'];
        if self.defaultConfigurationName == None:
            # this is a fall-back incase there is no default configuration set on the project level
            self.defaultConfigurationName = 'Release';
        self.name = self.defaultConfigurationName;
        
    def defaultBuildConfiguration(self):
        return self.buildConfigurationWithName(self.defaultConfigurationName)
    
    def buildConfigurationWithName(self, name):
        results = list(filter(lambda config: config.name == name, self.buildConfigurations))
        if len(results) == 0:
            results = self.buildConfigurations;
        return results[0];