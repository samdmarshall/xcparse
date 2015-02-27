from __future__ import absolute_import

class LaunchAction(object):
    # contents = {};
    # children = [];
    # selectedDebuggerIdentifier = '';
    # selectedLauncherIdentifier = '';
    # launchStyle = '';
    # useCustomWorkingDirectory = '';
    # buildConfiguration = '';
    # ignoresPersistentStateOnLaunch = '';
    # debugDocumentVersioning = '';
    # allowLocationSimulation = '';
    
    def __init__(self, action_xml):
        self.contents = action_xml;
        if 'selectedDebuggerIdentifier' in self.contents.keys():
            self.selectedDebuggerIdentifier = self.contents.get('selectedDebuggerIdentifier');
        if 'selectedLauncherIdentifier' in self.contents.keys():
            self.selectedLauncherIdentifier = self.contents.get('selectedLauncherIdentifier');
        if 'launchStyle' in self.contents.keys():
            self.launchStyle = self.contents.get('launchStyle');
        if 'useCustomWorkingDirectory' in self.contents.keys():
            self.useCustomWorkingDirectory = self.contents.get('useCustomWorkingDirectory');
        if 'buildConfiguration' in self.contents.keys():
            self.buildConfiguration = self.contents.get('buildConfiguration');
        if 'ignoresPersistentStateOnLaunch' in self.contents.keys():
            self.ignoresPersistentStateOnLaunch = self.contents.get('ignoresPersistentStateOnLaunch');
        if 'debugDocumentVersioning' in self.contents.keys():
            self.debugDocumentVersioning = self.contents.get('debugDocumentVersioning');
        if 'allowLocationSimulation' in self.contents.keys():
            self.allowLocationSimulation = self.contents.get('allowLocationSimulation');
        
    def performAction(self, container, project_constructor, scheme_config_settings):
        print 'implement me!';