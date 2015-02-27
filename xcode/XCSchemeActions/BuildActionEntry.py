from __future__ import absolute_import

from .BuildableReference import *

class BuildActionEntry(object):
    # contents = {};
    # buildForTesting = '';
    # buildForRunning = '';
    # buildForProfiling = '';
    # buildForArchiving = '';
    # buildForAnalyzing = '';
    # target = {};
    
    def __init__(self, entry_item):
        self.contents = entry_item;
        if 'buildForTesting' in self.contents.keys():
            self.buildForTesting = self.contents.get('buildForTesting');
        if 'buildForRunning' in self.contents.keys():
            self.buildForRunning = self.contents.get('buildForRunning');
        if 'buildForProfiling' in self.contents.keys():
            self.buildForProfiling = self.contents.get('buildForProfiling');
        if 'buildForArchiving' in self.contents.keys():
            self.buildForArchiving = self.contents.get('buildForArchiving');
        if 'buildForAnalyzing' in self.contents.keys():
            self.buildForAnalyzing = self.contents.get('buildForAnalyzing');
        self.target = BuildableReference(self.contents.find('./BuildableReference'));