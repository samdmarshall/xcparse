from __future__ import absolute_import

class ProfileAction(object):
    # contents = {};
    # children = [];
    # shouldUseLaunchSchemeArgsEnv = '';
    # savedToolIdentifier = '';
    # useCustomWorkingDirectory = '';
    # buildConfiguration = '';
    # debugDocumentVersioning = '';
    
    
    def __init__(self, action_xml):
        self.contents = action_xml;
        if 'shouldUseLaunchSchemeArgsEnv' in self.contents.keys():
            self.shouldUseLaunchSchemeArgsEnv = self.contents.get('shouldUseLaunchSchemeArgsEnv');
        if 'savedToolIdentifier' in self.contents.keys():
            self.savedToolIdentifier = self.contents.get('savedToolIdentifier');
        if 'useCustomWorkingDirectory' in self.contents.keys():
            self.useCustomWorkingDirectory = self.contents.get('useCustomWorkingDirectory');
        if 'buildConfiguration' in self.contents.keys():
            self.buildConfiguration = self.contents.get('buildConfiguration');
        if 'debugDocumentVersioning' in self.contents.keys():
            self.debugDocumentVersioning = self.contents.get('debugDocumentVersioning');
    
    def performAction(self, container, project_constructor, scheme_config_settings):
        print 'implement me!';