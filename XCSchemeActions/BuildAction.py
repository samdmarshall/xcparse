from __future__ import absolute_import
import xml.etree.ElementTree as xml

from .BuildActionEntry import *
from ..xcrun import *
from ..PBX.PBXResolver import *
from .Base_Action import *

class BuildAction(Base_Action):
    # contents = {};
    # children = [];
    # parallel = False;
    # implicit = False;
    
    def __init__(self, action_xml):
        self.contents = action_xml;
        if 'parallelizeBuildables' in self.contents.keys():
            self.parallel = self.contents.get('parallelizeBuildables');
        if 'buildImplicitDependencies' in self.contents.keys():
            self.implicit = self.contents.get('buildImplicitDependencies');
        self.children = list(map(lambda entry: BuildActionEntry(entry), list(self.contents.find('./BuildActionEntries'))));
        
    def performAction(self, build_system, container, project_constructor, scheme_config_settings):
        for child in self.children:
            project_path = xcrun.resolvePathFromLocation(child.target.ReferencedContainer, container[2].path.base_path, container[2].path.base_path);
            project = project_constructor(project_path);
            
            xcrun.perform_xcodebuild(project, container[1].name, 'build', scheme_config_settings);
            
            # target_constructor = PBXResolver(project.objects()[child.target.BlueprintIdentifier]);
            # if target_constructor[0] == True:
            #     target = target_constructor[1](PBXResolver, project.objects()[child.target.BlueprintIdentifier], project, child.target.BlueprintIdentifier);
            #     print target.name;
            #     for phase in target.buildPhases:
            #         phase.performPhase(build_system);