from __future__ import absolute_import

class BuildableReference(object):
    # contents = {};
    # BuildableIdentifier = '';
    # BlueprintIdentifier = '';
    # BuildableName = '';
    # BlueprintName = '';
    # ReferencedContainer = '';
    
    def __init__(self, entry_item):
        self.contents = entry_item;
        if 'BuildableIdentifier' in self.contents.keys():
            self.BuildableIdentifier = self.contents.get('BuildableIdentifier');
        if 'BlueprintIdentifier' in self.contents.keys():
            self.BlueprintIdentifier = self.contents.get('BlueprintIdentifier');
        if 'BuildableName' in self.contents.keys():
            self.BuildableName = self.contents.get('BuildableName');
        if 'BlueprintName' in self.contents.keys():
            self.BlueprintName = self.contents.get('BlueprintName');
        if 'ReferencedContainer' in self.contents.keys():
            self.ReferencedContainer = self.contents.get('ReferencedContainer');